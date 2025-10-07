from src.pipelines.datagen import DataGenFlow
import os
from loguru import logger

pod_name = os.getenv('POD_NAME')

def main():
    logger.info(f"Pod name: {pod_name}")
    data_gen = DataGenFlow()
    data_gen.run()
    logger.info("Data generation completed")
    
if __name__ == "__main__":
    main()