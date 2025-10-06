from src.pipelines.datagen import DataGenFlow
import os

pod_name = os.getenv('POD_NAME')

def main():
    data_gen = DataGenFlow()
    print(f"Pod name: {pod_name}")
    data_gen.run()
    
if __name__ == "__main__":
    main()