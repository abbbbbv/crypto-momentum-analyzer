# Crypto Momentum Analysis System

## Setup

### Installation

1. Clone or extract the project files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the analyzer:
```bash
python main.py
```

## Logic

The system analyzes cryptocurrency pairs using a multi-timeframe approach:

### Timeframes & Weights
- 15min (35% weight)
- 30min (25% weight) 
- 60min (20% weight)
- 240min (15% weight)
- 1Day (5% weight)

### Technical Indicators
- **RSI (20% weight)**: 14-period Relative Strength Index
- **Volume Momentum (25% weight)**: Recent vs average volume ratio
- **Price Change (15% weight)**: 20-period price change percentage
- **Base Bullish Score (40% weight)**: Neutral baseline weighting

### Scoring System
- **Bullish**: Score > 0.60
- **Neutral**: Score 0.40-0.60  
- **Bearish**: Score < 0.40

## Outputs

The system generates three types of outputs with datetime timestamps:

### 1. Reports (`reports/` folder)
- `crypto_momentum_insights_YYYYMMDD_HHMMSS.txt`
- Comprehensive text report with top performers, market statistics, sentiment breakdown, and trading signals

### 2. Visualizations (`visualizations/` folder)
- `momentum_score_rankings_YYYYMMDD_HHMMSS.png` - Overall score distribution
- `rsi_analysis_all_timeframes_YYYYMMDD_HHMMSS.png` - RSI analysis across timeframes
- `volume_analysis_all_timeframes_YYYYMMDD_HHMMSS.png` - Volume momentum analysis
- `score_distribution_YYYYMMDD_HHMMSS.png` - Score histogram
- `top_performers_YYYYMMDD_HHMMSS.png` - Top 20 ranked pairs
- `market_sentiment_YYYYMMDD_HHMMSS.png` - Bullish/Neutral/Bearish pie chart

### 3. Data Export (`exports/` folder)  
- `crypto_momentum_analysis_YYYYMMDD_HHMMSS.csv`
- Complete dataset with all indicators across timeframes

## File Structure

```
crypto-momentum-analyzer/
├── main.py                
├── requirements.txt       
├── README.md              
├── src/
│   ├── __init__.py
│   ├── crypto_analyzer.py  
│   ├── data_fetcher.py     
│   ├── report_generator.py 
│   ├── visualizer.py       
│   └── utils/
│       ├── __init__.py
│       └── file_manager.py 
├── reports/             
├── visualizations/        
└── exports/              
```

## Usage

The system runs continuously, performing analysis every 15 minutes. All outputs are automatically timestamped and organized in dedicated folders for easy management and historical tracking.

abhinav00345@gmail.com
