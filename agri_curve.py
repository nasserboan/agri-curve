from src.pipelines.datagen import DataGenFlow


def main():
    data_gen = DataGenFlow()
    data_gen.run()

if __name__ == "__main__":
    main()