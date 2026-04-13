import pandas as pd
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class StrategyBase(ABC):
    """
    Base class for all investment strategies.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the strategy."""
        pass
        
    @property
    @abstractmethod
    def default_parameters(self) -> Dict[str, Any]:
        """Default parameters for the strategy."""
        pass
        
    @abstractmethod
    def analyze(self, symbol: str, hist_data: pd.DataFrame, info_data: dict, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main analysis method.
        Must return a dict with:
        - is_opportunity (bool)
        - confidence (float 0-100)
        - current_price (float)
        - reason (str)
        - metrics (dict)
        """
        pass
