import asyncio
import aiohttp
import pandas as pd
import numpy as np
import ta
import time
from datetime import datetime
from typing import Dict, List, Optional
import warnings
from tqdm import tqdm
from .data_fetcher import DataFetcher
from .report_generator import ReportGenerator
from .visualizer import Visualizer
from .utils.file_manager import FileManager

warnings.filterwarnings('ignore')

class CryptoMomentumAnalyzer:
    def __init__(self, max_concurrent=15):
        self.data_fetcher = DataFetcher(max_concurrent)
        self.report_generator = ReportGenerator()
        self.visualizer = Visualizer()
        self.file_manager = FileManager()
        
        self.timeframes = {
            '15': {'weight': 0.35, 'resolution': '15'},
            '30': {'weight': 0.25, 'resolution': '30'},
            '60': {'weight': 0.20, 'resolution': '60'},
            '240': {'weight': 0.15, 'resolution': '240'},
            '1D': {'weight': 0.05, 'resolution': '1D'}
        }
        
        self.scoring_weights = {
            'base_bullish': 0.40,
            'rsi': 0.20,
            'volume': 0.25,
            'price_change': 0.15
        }
        
        self.results = {}
        self.pbar = None
        
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        if len(df) < 30:
            return None
            
        try:
            rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            
            recent_volume = df['volume'].iloc[-5:].mean()
            avg_volume = df['volume'].mean()
            volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
            
            price_change = ((df['close'].iloc[-1] - df['close'].iloc[-20]) / df['close'].iloc[-20]) * 100 if len(df) >= 20 else 0
            
            return {
                'rsi': current_rsi,
                'volume_ratio': volume_ratio,
                'price_change': price_change,
                'current_price': df['close'].iloc[-1],
                'volume': recent_volume
            }
            
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return None
    
    def calculate_momentum_score(self, timeframe_data: Dict) -> float:
        total_score = 0
        total_weight = 0
        
        for tf, data in timeframe_data.items():
            if data and data.get('indicators'):
                indicators = data['indicators']
                weight = self.timeframes[tf]['weight']
                
                base_score = 0.5
                
                rsi = indicators.get('rsi', 50)
                if 50 <= rsi <= 70:
                    rsi_score = 0.8
                elif 70 < rsi <= 80:
                    rsi_score = 0.6
                elif rsi > 80:
                    rsi_score = 0.3
                elif 40 <= rsi < 50:
                    rsi_score = 0.4
                else:
                    rsi_score = 0.2
                
                volume_ratio = indicators.get('volume_ratio', 1)
                volume_score = min(volume_ratio / 1.5, 1.0) if volume_ratio >= 1.5 else volume_ratio / 1.5
                
                price_change = indicators.get('price_change', 0)
                price_score = min(max(price_change / 10 + 0.5, 0), 1)
                
                tf_score = (base_score * self.scoring_weights['base_bullish'] +
                           rsi_score * self.scoring_weights['rsi'] +
                           volume_score * self.scoring_weights['volume'] +
                           price_score * self.scoring_weights['price_change'])
                
                total_score += tf_score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    async def analyze_pair(self, session: aiohttp.ClientSession, pair: str) -> Dict:
        """Analyze a single trading pair across all timeframes"""
        pair_data = {}
        
        for tf_key, tf_config in self.timeframes.items():
            df = await self.data_fetcher.fetch_candlestick_data(session, pair, tf_config['resolution'])
            if df is not None and len(df) > 0:
                indicators = self.calculate_technical_indicators(df)
                pair_data[tf_key] = {
                    'data': df,
                    'indicators': indicators
                }
        
        if self.pbar:
            self.pbar.update(1)
        
        if pair_data:
            momentum_score = self.calculate_momentum_score(pair_data)
            return {
                'pair': pair,
                'momentum_score': momentum_score,
                'timeframe_data': pair_data
            }
        
        return None
    
    async def run_analysis(self):
        print("Starting Crypto Momentum Analysis System")
        print("=" * 60)
        
        instruments = await self.data_fetcher.get_active_instruments()
        if not instruments:
            print("No instruments found. Exiting.")
            return
        
        print(f"Analyzing {len(instruments)} instruments across 5 timeframes...")
        
        self.pbar = tqdm(total=len(instruments), desc="Analyzing pairs", unit="pair")
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.analyze_pair(session, pair) for pair in instruments]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        self.pbar.close()
        
        valid_results = [r for r in results if r and not isinstance(r, Exception)]
        
        if not valid_results:
            print("No valid results obtained. Exiting.")
            return
        
        valid_results.sort(key=lambda x: x['momentum_score'], reverse=True)
        self.results = valid_results
        
        print(f"Analysis complete! Processed {len(valid_results)} pairs successfully")
        
        self.report_generator.generate_insights_report(self.results, self.timeframes)
        self.visualizer.create_visualizations(self.results, self.timeframes)
        self.file_manager.export_to_csv(self.results, self.timeframes)
        
        return valid_results