#!/usr/bin/env python3

import asyncio
import time
from datetime import datetime
from src.crypto_analyzer import CryptoMomentumAnalyzer

async def main():
    analyzer = CryptoMomentumAnalyzer(max_concurrent=15)
    results = await analyzer.run_analysis()
    return results

def run_scheduler():
    print("Starting scheduled crypto momentum analysis (every 15 minutes)")
    
    while True:
        try:
            results = asyncio.run(main())
            
            current_time = datetime.now()
            next_run = current_time.replace(second=0, microsecond=0)
            
            minute = next_run.minute
            next_minute = ((minute // 15) + 1) * 15
            if next_minute >= 60:
                next_run = next_run.replace(hour=next_run.hour + 1, minute=0)
            else:
                next_run = next_run.replace(minute=next_minute)
            
            sleep_seconds = (next_run - current_time).total_seconds()
            print(f"Next analysis at {next_run.strftime('%H:%M:%S')} (sleeping for {sleep_seconds:.0f} seconds)")
            time.sleep(max(sleep_seconds, 0))
            
        except KeyboardInterrupt:
            print("\nAnalysis stopped by user")
            break
        except Exception as e:
            print(f"Error in scheduler: {str(e)}")
            time.sleep(60)

if __name__ == "__main__":
    run_scheduler()