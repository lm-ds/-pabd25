import datetime
import cianparser
import pandas as pd

moscow_parser = cianparser.CianParser(location="Москва")


def main():
    t = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    for i in range(1, 4):
        file_path = f"-pabd25/data/row/room_{i}_{t}.csv"
        data = moscow_parser.get_flats(
            deal_type="sale", 
            rooms=(i,), 
            with_saving_csv=False, 
            additional_settings={
                "start_page": 1, 
                "end_page": 5,
                "object_type": "secondary"
            }
        )
        df = pd.DataFrame(data)
        df.to_csv(file_path, encoding="utf-8", index=False)


if __name__ == "__main__":
    main()