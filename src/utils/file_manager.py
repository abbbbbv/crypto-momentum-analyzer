import pandas as pd
import os
from datetime import datetime
from typing import List, Dict

class FileManager:
    def __init__(self):
        self.exports_dir = "exports"
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        if not os.path.exists(self.exports_dir):
            os.makedirs(self.exports_dir)
    
    def export_to_csv(self, results: List[Dict], timeframes: Dict):
        """Export results to CSV file"""
        if not results:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_data = []
        
        for result in results:
            pair = result['pair'].replace('B-', '').replace('_USDT', '/USDT')
            
            row = {
                'Pair': pair,
                'Momentum_Score': result['momentum_score'],
                'Rank': len(export_data) + 1
            }
            
            for tf in timeframes.keys():
                if tf in result['timeframe_data'] and result['timeframe_data'][tf]['indicators']:
                    indicators = result['timeframe_data'][tf]['indicators']
                    row[f'RSI_{tf}'] = indicators.get('rsi', None)
                    row[f'Volume_Ratio_{tf}'] = indicators.get('volume_ratio', None)
                    row[f'Price_Change_{tf}'] = indicators.get('price_change', None)
                else:
                    row[f'RSI_{tf}'] = None
                    row[f'Volume_Ratio_{tf}'] = None
                    row[f'Price_Change_{tf}'] = None
            
            export_data.append(row)
        
        df = pd.DataFrame(export_data)
        filename = os.path.join(self.exports_dir, f"crypto_momentum_analysis_{timestamp}.csv")
        df.to_csv(filename, index=False)
        
        print(f"Data exported to '{filename}'")