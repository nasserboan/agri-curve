from src.pipelines.datagen import DataGenFlow
from loguru import logger

def main():
    data_gen = DataGenFlow()
    data_gen.run()
    logger.info("Data generation completed")
    
if __name__ == "__main__":
    main()