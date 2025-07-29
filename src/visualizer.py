import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from typing import List, Dict

plt.style.use('seaborn-v0_8-darkgrid')

class Visualizer:
    def __init__(self):
        self.visualizations_dir = "visualizations"
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        if not os.path.exists(self.visualizations_dir):
            os.makedirs(self.visualizations_dir)
    
    def create_visualizations(self, results: List[Dict], timeframes: Dict):
        if not results:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        pairs = [r['pair'].replace('B-', '').replace('_USDT', '') for r in results]
        scores = [r['momentum_score'] for r in results]
        
        timeframe_data = {}
        for tf in timeframes.keys():
            rsi_data = []
            volume_data = []
            price_change_data = []
            
            for result in results:
                if tf in result['timeframe_data'] and result['timeframe_data'][tf]['indicators']:
                    indicators = result['timeframe_data'][tf]['indicators']
                    rsi_data.append(indicators.get('rsi', 50))
                    volume_data.append(indicators.get('volume_ratio', 1))
                    price_change_data.append(indicators.get('price_change', 0))
                else:
                    rsi_data.append(50)
                    volume_data.append(1)
                    price_change_data.append(0)
            
            timeframe_data[tf] = {
                'rsi': rsi_data,
                'volume': volume_data,
                'price_change': price_change_data
            }
        
        # 1. Momentum Score Distribution
        plt.figure(figsize=(12, 8))
        colors = ['red' if s < 0.4 else 'orange' if s < 0.6 else 'green' for s in scores]
        bars = plt.bar(range(len(scores)), scores, color=colors, alpha=0.7)
        plt.title('Momentum Score Rankings', fontsize=16, fontweight='bold')
        plt.xlabel('Trading Pairs (Ranked)')
        plt.ylabel('Momentum Score')
        plt.axhline(y=0.6, color='green', linestyle='--', alpha=0.7, label='Bullish Threshold')
        plt.axhline(y=0.4, color='red', linestyle='--', alpha=0.7, label='Bearish Threshold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'momentum_score_rankings_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. RSI Analysis for all timeframes
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, (tf, data) in enumerate(timeframe_data.items()):
            if i < len(axes):
                scatter_colors = ['red' if s < 0.4 else 'orange' if s < 0.6 else 'green' for s in scores]
                axes[i].scatter(data['rsi'], scores, c=scatter_colors, alpha=0.6, s=30)
                axes[i].axvline(x=50, color='blue', linestyle='--', alpha=0.5, label='RSI 50')
                axes[i].axvline(x=70, color='orange', linestyle='--', alpha=0.5, label='RSI 70')
                axes[i].axhline(y=0.6, color='green', linestyle='--', alpha=0.5, label='Bullish Score')
                axes[i].set_title(f'RSI Analysis - {tf}min' if tf != '1D' else 'RSI Analysis - Daily')
                axes[i].set_xlabel('RSI (14-period)')
                axes[i].set_ylabel('Momentum Score')
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)
        
        if len(timeframe_data) < len(axes):
            fig.delaxes(axes[-1])
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'rsi_analysis_all_timeframes_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Volume Analysis for all timeframes
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, (tf, data) in enumerate(timeframe_data.items()):
            if i < len(axes):
                volume_colors = ['lightcoral' if v < 1.5 else 'lightgreen' for v in data['volume']]
                axes[i].scatter(data['volume'], scores, c=volume_colors, alpha=0.6, s=30)
                axes[i].axvline(x=1.5, color='red', linestyle='--', alpha=0.7, label='High Volume Threshold(1.5x)')
                axes[i].set_title(f'Volume Analysis - {tf}min' if tf != '1D' else 'Volume Analysis - Daily')
                axes[i].set_xlabel('Volume Ratio (Recent/Average)')
                axes[i].set_ylabel('Momentum Score')
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)
        
        if len(timeframe_data) < len(axes):
            fig.delaxes(axes[-1])
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'volume_analysis_all_timeframes_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Score Distribution Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=30, color='skyblue', alpha=0.7, edgecolor='black')
        plt.axvline(x=np.mean(scores), color='red', linestyle='-', linewidth=2, label=f'Mean: {np.mean(scores):.3f}')
        plt.axvline(x=np.median(scores), color='green', linestyle='-', linewidth=2, label=f'Median: {np.median(scores):.3f}')
        plt.title('Momentum Score Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Momentum Score')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'score_distribution_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Top 20 Performers
        plt.figure(figsize=(12, 10))
        top_20_pairs = pairs[:20]
        top_20_scores = scores[:20]
        colors_top20 = plt.cm.RdYlGn([s for s in top_20_scores])
        
        bars = plt.barh(range(len(top_20_pairs)), top_20_scores, color=colors_top20)
        plt.yticks(range(len(top_20_pairs)), top_20_pairs)
        plt.title('Top 20 Momentum Leaders', fontsize=16, fontweight='bold')
        plt.xlabel('Momentum Score')
        plt.grid(True, alpha=0.3)
        
        for i, (bar, score) in enumerate(zip(bars, top_20_scores)):
            plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{score:.3f}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'top_performers_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 6. Market Sentiment Pie Chart
        plt.figure(figsize=(8, 8))
        bullish_count = sum(1 for s in scores if s > 0.6)
        neutral_count = sum(1 for s in scores if 0.4 <= s <= 0.6)
        bearish_count = sum(1 for s in scores if s < 0.4)
        
        sizes = [bullish_count, neutral_count, bearish_count]
        labels = ['Bullish', 'Neutral', 'Bearish']
        colors = ['green', 'orange', 'red']
        explode = (0.1, 0, 0)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.title('Market Sentiment Distribution', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(self.visualizations_dir, f'market_sentiment_{timestamp}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualizations saved in '{self.visualizations_dir}' directory with timestamp {timestamp}")