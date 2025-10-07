from metaflow import FlowSpec, step, Parameter, parallel
from config.config import DATA_GEN_CONFIG
from src.nodes.datagen import generate_logistics_transport_data


class DataGenFlow(FlowSpec):
    """
    Data Generation Pipeline
    
    Generates synthetic logistics transport data for model training.
    
    Usage:
        python -m src.pipelines.datagen run
        python -m src.pipelines.datagen run --num_operations 100000 --seed 12345
    """
    
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
    
    data_dir = Parameter(
        'data_dir',
        default=DATA_GEN_CONFIG.data_dir,
        type=str,
        help='Output directory for generated data'
    )

    @step
    def start(self):
        self.next(self.generate_data)

    @step
    def generate_data(self):
        self.data = generate_logistics_transport_data(
            num_operations=self.num_operations,
            seed=self.seed,
            data_dir=self.data_dir
        )
        
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    DataGenFlow()