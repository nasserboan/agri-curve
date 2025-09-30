from pydantic_settings import BaseSettings

class DataGenConfig(BaseSettings):

    num_operations: int = 1_000
    seed: int = 424242
    data_dir: str = 'data/raw'
    output_filename: str = 'logistics_transport_data.csv'

class PreprocessConfig(BaseSettings):
    input_filename: str = 'logistics_transport_data.csv'
    input_data_dir: str = 'data/raw'
    seed: int = 424242
    test_size: float = 0.2
    data_dir: str = 'data/processed'

DATA_GEN_CONFIG = DataGenConfig()