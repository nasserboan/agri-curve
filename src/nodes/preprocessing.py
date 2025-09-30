import pandas as pd
from typing import Tuple
from sklearn.base import BaseEstimator, TransformerMixin
from loguru import logger


class DateFilter(BaseEstimator, TransformerMixin):
    def __init__(self, date_column: str, date_str_format: str = '%Y-%m-%d', start_date: str = None, end_date: str = None):
    
        self.date_column = date_column
        self.date_str_format = date_str_format
        self.start_date = start_date
        self.end_date = end_date

        self._check_start_end_date()
    
    def fit(self, X: pd.DataFrame, y=None):
       
       ## check if the date column exists
        if self._check_date_column(X):
            self.data = X
        else:
            raise ValueError(f"Date column {self.date_column} not found in DataFrame")
        
        ## check if the date column is a datetime column, 
        ## if not, convert it to datetime using the date_str_format
        self._check_date_column_type(self.date_str_format)

        ## check if the start and end date are valid
        self._check_start_end_date()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.query(f"{self.date_column} >= @self.start_date and {self.date_column} <= @self.end_date")

    def _check_date_column(self, X: pd.DataFrame) -> bool:
        if self.date_column not in X.columns:
            raise ValueError(f"Date column {self.date_column} not found in DataFrame")
        return True

    def _check_date_column_type(self, date_str_format: str) -> bool:
        if not pd.api.types.is_datetime64_any_dtype(self.data[self.date_column]):
            logger.warning(f"Date column {self.date_column} is not a datetime column, it will be converted to datetime")
            self.data[self.date_column] = pd.to_datetime(self.data[self.date_column], format=date_str_format)
        return True

    def _check_start_end_date(self) -> bool:
        if self.start_date is not None and self.end_date is not None:
            
            if isinstance(self.start_date, str):
                self.start_date = pd.to_datetime(self.start_date, format=self.date_str_format)
            if isinstance(self.end_date, str):
                self.end_date = pd.to_datetime(self.end_date, format=self.date_str_format)
            
            if self.start_date >= self.end_date:
                raise ValueError(f"Start date {self.start_date} is greater than end date {self.end_date}")
        else:
            logger.warning("Start and end date are not set, all dates will be kept")
        return True






def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    pass

def generate_seasonality_features(df: pd.DataFrame) -> pd.DataFrame:
    pass