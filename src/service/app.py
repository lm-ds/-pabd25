from flask import Flask, render_template, request
import logging 


app = Flask(__name__)

logger = logging.getLogger(name=None)
logger.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
to_file = logging.FileHandler('-pabd25/src/service/log.txt', encoding='utf-8')
to_file.setLevel(logging.INFO)
to_file.setFormatter(format)
logger.addHandler(to_file)

to_console = logging.StreamHandler()
to_console.setLevel(logging.INFO)
to_console.setFormatter(format)
logger.addHandler(to_console)

# Маршрут для отображения формы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для обработки данных формы
@app.route('/api/numbers', methods=['POST'])
def process_numbers():
    # Здесь можно добавить обработку полученных чисел
    # Для примера просто возвращаем их обратно
    numbers = request.get_json()
    area = int(numbers['area'])
    rooms = int(numbers['rooms'])
    floors = int(numbers['floors'])
    floor = int(numbers['floor'])
    price = 300000 * int(area)

    logging.info(f'Полученные данные: Площадь квартиры, кв.м. = {area}, Кол-во комнат = {rooms}, Этажей в доме = {floors}, Желаемый этаж = {floor}')

    if floors < floor:
        error_msg = 'Выбранный этаж квартиры не может быть больше общего числа этажей.'
        return {'Price' : error_msg}
    else:
        logging.info(f'Расчётная цена: {price}')
        return {'Price' : price}



if __name__ == '__main__':
    app.run(debug=True)