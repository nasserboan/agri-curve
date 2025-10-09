from pydantic_settings import BaseSettings

class DataGenConfig(BaseSettings):
    num_operations: int = 500_000
    seed: int = 424242
    output_dir: str = 'data/raw'
    file_name: str = 'logistics_transport_data.csv'
    base_date: str = '2023-01-01'
    range_days: int = 720

class PreprocessConfig(BaseSettings):
    input_filename: str = 'logistics_transport_data.csv'
    input_data_dir: str = 'data/raw'
    seed: int = 424242
    date_column: str = 'operation_date'
    date_str_format: str = '%Y-%m-%d'
    filter_start_date: str = '2023-01-01'
    filter_end_date: str = '2023-12-31'
    

DATA_GEN_CONFIG = DataGenConfig()