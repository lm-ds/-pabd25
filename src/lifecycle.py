import os
import cianparser
import pandas as pd
import glob
import numpy as np
import os
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import argparse
import datetime


os.makedirs("/Users/lubovmoskalenko/Documents/python/-pabd25/src/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/Users/lubovmoskalenko/Documents/python/-pabd25/src/logs/lifecycle.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def parse_cian():
    moscow_parser = cianparser.CianParser(location="Москва")
    t = datetime.datetime.now().strftime("%Y-%m-%d")
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


def preprocess_data():
    raw_data_path = "/Users/lubovmoskalenko/Documents/python/-pabd25/data/row/"
    file_list = glob.glob(os.path.join(raw_data_path, "*.csv"))

    dataframes = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"Ошибка при чтении {file}: {e}")
    main_dataframe = pd.concat(dataframes, ignore_index=True)
    main_dataframe["url_id"] = main_dataframe["url"].map(lambda x: x.split("/")[-2] if isinstance(x, str) else None)
    df = main_dataframe[["url_id", "total_meters", "floor", "floors_count", "rooms_count", "price"]].dropna().set_index("url_id")

    df = df[(df["total_meters"] <= 300) & (df["price"] < 100_000_000)]
    # df = df.drop(columns=['url_id'])

    df.to_csv("/Users/lubovmoskalenko/Documents/python/-pabd25/data/processed/merged_cleaned.csv", encoding="utf-8")


def train():
    data = pd.read_csv("/Users/lubovmoskalenko/Documents/python/-pabd25/data/processed/merged_cleaned.csv")
    
    X = data[["total_meters", "floor", "floors_count", "rooms_count"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = np.mean(np.abs(y_test - y_pred))

    logging.info(f"Среднеквадратичная ошибка (MSE): {mse:.2f}")
    logging.info(f"Корень из MSE (RMSE): {rmse:.2f}")
    logging.info(f"Коэффициент детерминации R²: {r2:.6f}")
    logging.info(f"Средняя абсолютная ошибка (MAE): {mae:.2f} рублей")
    logging.info(f"Коэффициент при площади: {model.coef_[0]:.2f}")
    logging.info(f"Свободный член (intercept): {model.intercept_:.2f}")

    os.makedirs("models", exist_ok=True)
    model_path = f"models/linear_regression_model.pkl"

    joblib.dump(model, model_path)


def test():
    model_path = f"models/linear_regression_model.pkl"
    model = joblib.load(model_path)

    data = [
        {"total_meters": 45, "floor": 2, "floors_count": 5, "rooms_count": 2},
        {"total_meters": 60, "floor": 4, "floors_count": 9, "rooms_count": 3},
        {"total_meters": 30, "floor": 1, "floors_count": 3, "rooms_count": 1},
        {"total_meters": 80, "floor": 6, "floors_count": 12, "rooms_count": 4},
    ]

    input_df = pd.DataFrame(data)

    # Предсказание
    predicted_prices = model.predict(input_df)

    logging.info("=== Предсказания модели по массиву данных ===")
    for features, price in zip(data, predicted_prices):
        log_msg = (
            f"Площадь: {features['total_meters']} м², "
            f"Комнат: {features['rooms_count']}, "
            f"Этаж: {features['floor']}/{features['floors_count']} → "
            f"Цена: {price:,.0f} ₽"
        )
        logging.info(log_msg)



if __name__ == "__main__":
    """Parse arguments and run lifecycle steps"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Model name")
    parser.add_argument(
        "-p",
        "--pages",
        type=int,
        help="Amount of pages to parse",
    )
    args = parser.parse_args()
    # parse_cian(args.pages)
    preprocess_data()
    train()
    test()