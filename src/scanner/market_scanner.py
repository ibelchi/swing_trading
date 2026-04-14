import logging
import time
import pandas as pd
import yfinance as yf
from typing import Optional

from src.data.ingestion import get_market_symbols, get_historical_data, get_company_info, get_detailed_info, RateLimitException
from src.database.db import SessionLocal, Opportunity, StrategyConfig
from src.strategies.buy_the_dip import BuyTheDipStrategy

logger = logging.getLogger(__name__)

class MarketScanner:
    def __init__(self):
        # List of active plugins
        self.strategies = [
            BuyTheDipStrategy()
        ]
        
    def run_scan(self, market: str = "sp500", limit_symbols: Optional[int] = None, on_opportunity_found=None):
        """
        Executes all active strategies over the appropriate market symbols.
        :param market: Market code to scan.
        :param limit_symbols: Limit the number of stocks to scan (useful for testing)
        :param on_opportunity_found: Optional callback function triggered when an opportunity is found.
        """
        logger.info(f"Starting Market Scanner ({market})...")
        symbols = get_market_symbols(market)
        
        if not symbols or len(symbols) == 0:
            raise RuntimeError(f"The scanner was unable to obtain any base list of symbols for the {market} market. Please check the data source.")
            
        if limit_symbols:
            symbols = symbols[:limit_symbols]
            
        logger.info(f"Scanning {len(symbols)} symbols...")
        
        # Download SPY data once for systemic market analysis
        spy_data = pd.DataFrame()
        try:
            spy_data = get_historical_data("SPY", period="2y")
            if spy_data.empty:
                logger.warning("Could not download SPY data. Relative market analysis will be disabled.")
            else:
                logger.info("SPY data downloaded successfully for market context.")
        except Exception as e:
            logger.warning(f"Initial SPY Context fetch failed: {e}. Moving on without market relative analysis.")
        
        db = SessionLocal()
        try:
            for strategy in self.strategies:
                # Retrieve parameters from DB if available, otherwise use defaults
                config_record = db.query(StrategyConfig).filter(StrategyConfig.strategy_name == strategy.name).first()
                config = config_record.parameters if config_record else strategy.default_parameters
                
                logger.info(f"Executing strategy: {strategy.name}")
                
                # 1. PRE-FETCH DATA IN BATCHES (Avoids 429 errors from too many requests)
                logger.info(f"Pre-fetching data for {len(symbols)} symbols in batches...")
                batch_size = 30
                all_hist_data = {}
                for i in range(0, len(symbols), batch_size):
                    batch = symbols[i:i+batch_size]
                    try:
                        logger.info(f"Downloading batch {i//batch_size + 1}/{(len(symbols)-1)//batch_size + 1}...")
                        data = yf.download(batch, period="1y", group_by='ticker', progress=False, timeout=30)
                        for sym in batch:
                            if len(batch) > 1:
                                if sym in data.columns.levels[0]:
                                    all_hist_data[sym] = data[sym].dropna(how='all')
                            else:
                                all_hist_data[sym] = data.dropna(how='all')
                    except Exception as e:
                        logger.warning(f"Batch download failed for {batch}: {e}")
                    
                    time.sleep(2.0) # Small break between batches

                logger.info("Starting individual analysis...")
                for idx, sym in enumerate(symbols):
                    try:
                        if idx % 20 == 0 and idx > 0:
                            logger.info(f"Progress: {idx}/{len(symbols)} scanned.")
                            
                        # Retrieve pre-fetched data
                        hist_data = all_hist_data.get(sym, pd.DataFrame())
                        
                        # Fallback to individual if batch failed/missing
                        if hist_data.empty:
                            hist_data = get_historical_data(sym)
                            time.sleep(1.0) # Additional delay for individual fallback

                        info_data = get_company_info(sym)
                        
                        if hist_data.empty:
                            if on_opportunity_found:
                                on_opportunity_found(sym, None, {"is_opportunity": False, "reason": "No historical data available"})
                            continue
                            
                        # Execute plugin strategy logic
                        result = strategy.analyze(sym, hist_data, info_data, config, spy_hist_data=spy_data)
                        
                        if result.get("is_opportunity"):
                            logger.info(f"-> SUCCESS {sym} | Conf: {result.get('confidence')}%")
                            
                            # 3. EXTRA FETCH (Only for winners) - Fetch full name/sector
                            detailed = get_detailed_info(sym)
                            
                            op = Opportunity(
                                symbol=sym,
                                company_name=detailed.get("short_name") or info_data.get("short_name") or sym,
                                strategy_name=strategy.name,
                                current_price=result.get("current_price"),
                                strategy_config=config,
                                explanation=result.get("reason"),
                                metrics=result.get("metrics"),
                                confidence=result.get("confidence", 0.0),
                                market=market,
                                currency=info_data.get("currency", "USD")
                            )
                            # Update metrics with detailed info
                            op.metrics.update(detailed)
                            db.add(op)
                            db.commit()
                            
                        # Trigger UI callback for BOTH success and filtered items (Transparency)
                        if on_opportunity_found:
                            on_opportunity_found(sym, hist_data, result)
                            
                    except RateLimitException as rle:
                        logger.warning(f"RATE LIMIT: {rle}. Pausing scan for 60 seconds...")
                        if on_opportunity_found:
                             on_opportunity_found(sym, None, {"is_opportunity": False, "reason": "Paused: Rate Limit hit"})
                        time.sleep(60) # Massive pause to let Yahoo breathe
                        db.rollback()
                        # Do NOT raise, just continue to next symbol (which will wait again)
                    except Exception as e:
                        logger.error(f"Error analyzing symbol {sym} with {strategy.name}: {e}")
                        if on_opportunity_found:
                            on_opportunity_found(sym, None, {"is_opportunity": False, "reason": f"System error: {str(e)[:50]}"})
                        db.rollback()
                        
        finally:
            db.close()
            logger.info("Market Scan completed!")
