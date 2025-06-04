from flask import Flask, jsonify, render_template, request
import logging 
import joblib
import pandas as pd
import subprocess
import argparse


app = Flask(__name__)

logger = logging.getLogger(name=None)
logger.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
to_file = logging.FileHandler("-pabd25/models learn/logs/app_logs.log", encoding="utf-8")
to_file.setLevel(logging.INFO)
to_file.setFormatter(format)
logger.addHandler(to_file)

to_console = logging.StreamHandler()
to_console.setLevel(logging.INFO)
to_console.setFormatter(format)
logger.addHandler(to_console)


def format_price(price):
    millions = int(price // 1_000_000)
    thousands = int((price % 1_000_000) // 1_000)
    return (
        f"{millions} миллион {thousands} тысяч"
        if millions > 0
        else f"{thousands} тысяч"
    )


def load_model(): 
    try:
        model = joblib.load(f"models/linear_regression_model.pkl")
        return model
    except FileNotFoundError:
        raise



# Маршрут для отображения формы
@app.route("/")
def index():
    return render_template("index.html")


# Маршрут для обработки данных формы
@app.route("/api/numbers", methods=["POST"])
def process_numbers():
    # Здесь можно добавить обработку полученных чисел
    # Для примера просто возвращаем их обратно
    numbers = request.get_json()
    area = int(numbers["area"])
    rooms = int(numbers["rooms"])
    floors = int(numbers["floors"])
    floor = int(numbers["floor"])
    input_df = pd.DataFrame({"total_meters": [area]})
    predicted_price = model.predict(input_df)[0]
    formatted_price = format_price(predicted_price)
    logging.info(f"Полученные данные: Площадь квартиры, кв.м. = {area}, Кол-во комнат = {rooms}, Этажей в доме = {floors}, Желаемый этаж = {floor}")

    if floors < floor:
        error_msg = "Выбранный этаж квартиры не может быть больше общего числа этажей."
        return {"Price" : error_msg}
    else:
        logging.info(f"Расчётная цена: {formatted_price}")
        return {"Price" : formatted_price}


if __name__ == '__main__':
    app.run(debug=True)
    model = load_model()