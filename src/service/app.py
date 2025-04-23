from flask import Flask, render_template, request

app = Flask(__name__)

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
    print(numbers['area'])
    price = int(numbers['area']) + int(numbers['rooms']) + int(numbers['floors']) + int(numbers['floor'])
    return {'price' : price}

if __name__ == '__main__':
    app.run(debug=True)