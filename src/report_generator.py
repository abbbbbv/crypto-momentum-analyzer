import numpy as np
import os
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_insights_report(self, results: List[Dict], timeframes: Dict):
        if not results:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.reports_dir, f"crypto_momentum_insights_{timestamp}.txt")
        
        with open(filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CRYPTO MOMENTUM ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"Total Pairs Analyzed: {len(results)}\n")
            f.write("\n")
            
            f.write("TOP 10 MOMENTUM PERFORMERS\n")
            f.write("-" * 50 + "\n")
            for i, result in enumerate(results[:10], 1):
                pair = result['pair'].replace('B-', '').replace('_USDT', '/USDT')
                score = result['momentum_score']
                
                current_price = "N/A"
                if '15' in result['timeframe_data'] and result['timeframe_data']['15']['indicators']:
                    current_price = f"${result['timeframe_data']['15']['indicators']['current_price']:.4f}"
                
                f.write(f"{i:2d}. {pair:15} | Score: {score:.3f} | Price: {current_price}\n")
            
            scores = [r['momentum_score'] for r in results]
            f.write(f"\nMARKET STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Average Momentum Score: {np.mean(scores):.3f}\n")
            f.write(f"Median Momentum Score:  {np.median(scores):.3f}\n")
            f.write(f"Highest Score:          {max(scores):.3f}\n")
            f.write(f"Lowest Score:           {min(scores):.3f}\n")
            f.write(f"Standard Deviation:     {np.std(scores):.3f}\n")
            
            bullish_count = sum(1 for score in scores if score > 0.6)
            neutral_count = sum(1 for score in scores if 0.4 <= score <= 0.6)
            bearish_count = sum(1 for score in scores if score < 0.4)
            
            f.write(f"\nMARKET SENTIMENT BREAKDOWN\n")
            f.write("-" * 35 + "\n")
            f.write(f"Strongly Bullish (>0.60): {bullish_count:3d} pairs ({bullish_count/len(scores)*100:.1f}%)\n")
            f.write(f"Neutral (0.40-0.60):      {neutral_count:3d} pairs ({neutral_count/len(scores)*100:.1f}%)\n")
            f.write(f"Bearish (<0.40):          {bearish_count:3d} pairs ({bearish_count/len(scores)*100:.1f}%)\n")
            
            f.write(f"\nTIMEFRAME ANALYSIS\n")
            f.write("-" * 25 + "\n")
            for tf, config in timeframes.items():
                tf_name = f"{tf}min" if tf != '1D' else "1Day"
                f.write(f"{tf_name:6} Weight: {config['weight']*100:4.1f}%\n")
            
            f.write(f"\nACTIONABLE TRADING SIGNALS\n")
            f.write("-" * 40 + "\n")
            
            strong_buy = [r for r in results if r['momentum_score'] > 0.7]
            buy = [r for r in results if 0.6 < r['momentum_score'] <= 0.7]
            
            if strong_buy:
                f.write("STRONG BUY SIGNALS:\n")
                for result in strong_buy[:5]:
                    pair = result['pair'].replace('B-', '').replace('_USDT', '/USDT')
                    score = result['momentum_score']
                    f.write(f"   • {pair} (Score: {score:.3f})\n")
            
            if buy:
                f.write("BUY SIGNALS:\n")
                for result in buy[:5]:
                    pair = result['pair'].replace('B-', '').replace('_USDT', '/USDT')
                    score = result['momentum_score']
                    f.write(f"   • {pair} (Score: {score:.3f})\n")
            
            if not strong_buy and not buy:
                f.write("No strong buy signals detected in current market conditions\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("Report generated successfully!\n")
            f.write("=" * 80 + "\n")
        
        print(f"Insights report saved to '{filename}'")