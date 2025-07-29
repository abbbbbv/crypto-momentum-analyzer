import asyncio
import aiohttp
import pandas as pd
import time
from typing import List, Optional

class DataFetcher:
    def __init__(self, max_concurrent=15):
        self.base_url = "https://public.coindcx.com/market_data/candlesticks"
        self.active_instruments_url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments?margin_currency_short_name[]=USDT"
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def get_active_instruments(self) -> List[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.active_instruments_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        instruments = [item for item in data if isinstance(item, str) and 'USDT' in item]
                        print(f"Found {len(instruments)} active USDT instruments")                
                        return instruments
                    else:
                        print(f"Failed to fetch instruments: {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching instruments: {str(e)}")
            return []
    
    async def fetch_candlestick_data(self, session: aiohttp.ClientSession, 
                                   pair: str, timeframe: str, periods: int = 100) -> Optional[pd.DataFrame]:
        async with self.semaphore:
            try:
                end_time = int(time.time())
                
                if timeframe == '1D':
                    start_time = end_time - (periods * 24 * 60 * 60)
                elif timeframe in ['15', '30', '60', '240']:
                    minutes = int(timeframe)
                    start_time = end_time - (periods * minutes * 60)
                else:
                    start_time = end_time - (periods * 60 * 60)
                
                params = {
                    'pair': pair,
                    'from': start_time,
                    'to': end_time,
                    'resolution': timeframe,
                    'pcode': 'f'
                }
                
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('s') == 'ok' and data.get('data'):
                            df = pd.DataFrame(data['data'])
                            df['timestamp'] = pd.to_datetime(df['time'], unit='ms')
                            df = df.sort_values('timestamp')
                            return df
                    
                    await asyncio.sleep(0.1)
                    return None
                    
            except Exception as e:
                print(f"Error fetching {pair} {timeframe}: {str(e)}")
                return None