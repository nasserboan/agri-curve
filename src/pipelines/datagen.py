from metaflow import FlowSpec, step, Parameter, parallel
from config.config import DATA_GEN_CONFIG
from src.nodes.datagen import DataGenerator
from loguru import logger
import os


class DataGenFlow(FlowSpec):

    num_operations = Parameter(
        'num_operations',
        default=DATA_GEN_CONFIG.num_operations,
        type=int,
        help='Number of transport operations to generate'
    )
    
    seed = Parameter(
        'seed',
        default=DATA_GEN_CONFIG.seed,
        type=int,
        help='Random seed for reproducibility'
    )
    
    output_dir = Parameter(
        'output_dir',
        default=DATA_GEN_CONFIG.output_dir,
        type=str,
        help='Output directory for generated data'
    )

    file_name = Parameter(
        'file_name',
        default=DATA_GEN_CONFIG.file_name,
        type=str,
        help='Name for the output file'
    )

    base_date = Parameter(
        'base_date',
        default=DATA_GEN_CONFIG.base_date,
        type=str,
        help='Base date for the operation date generation'
    )

    range_days = Parameter(
        'range_days',
        default=DATA_GEN_CONFIG.range_days,
        type=int,
        help='Number of days for the operation dates'
    )

    @step
    def start(self):
        self.generator_class = DataGenerator(
            num_operations=self.num_operations,
            seed=self.seed,
            output_dir=self.output_dir,
            file_name=self.file_name,
            base_date=self.base_date,
            range_days=self.range_days
        )
        logger.info(f"Absolute path: {os.path.abspath(self.output_dir)}")
        self.next(self.generate_data)

    @step
    def generate_data(self):
        self.data = self.generator_class.generate()
        self.next(self.end)

    @step
    def end(self):
        pass