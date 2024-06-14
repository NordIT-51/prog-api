from flask import Flask, request, jsonify, abort
from datetime import datetime

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Пример списка фильмов
movies = [
    {
        "id": 1,
        "title": "Побег из Шоушенка",
        "year": 1994,
        "director": "Фрэнк Дарабонт",
        "length": "02:22:00",
        "rating": 9
    },
    {
        "id": 2,
        "title": "Крёстный отец",
        "year": 1972,
        "director": "Фрэнсис Форд Коппола",
        "length": "02:55:00",
        "rating": 9
    }
]

# Функция для валидации данных фильма
def validate(data):
    if 'id' not in data or not isinstance(data['id'], int):
        return "Поле 'id' не задано или задано некорректно"
    if 'title' not in data or not isinstance(data['title'], str) or len(data['title']) > 100:
        return "Поле 'title' не задано или задано некорректно"
    if 'year' not in data or not isinstance(data['year'], int) or not (1900 <= data['year'] <= 2100):
        return "Поле 'year' не задано или задано некорректно"
    if 'director' not in data or not isinstance(data['director'], str) or len(data['director']) > 100:
        return "Поле 'director' не задано или задано некорректно"
    if 'length' not in data or not isinstance(data['length'], str):
        try:
            datetime.strptime(data['length'], '%H:%M:%S')
        except ValueError:
            return "Неверный формат поля 'length', должно быть: 'HH:MM:SS'"
    if 'rating' not in data or not isinstance(data['rating'], int) or not (0 <= data['rating'] <= 10):
        return "Поле 'rating' не задано или задано некорректно"
    return None

# Маршрут для получения списка всех фильмов
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify({"list": movies}), 200

# Маршрут для получения информации о конкретном фильме по ID
@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = next((movie for movie in movies if movie['id'] == id), None)
    if movie is None:
        abort(404)
    return jsonify({"movie": movie}), 200

# Маршрут для добавления нового фильма
@app.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.json.get('movie', {})
    validation_error = validate(data)
    if validation_error:
        return jsonify({"status": 400, "reason": validation_error}), 400
    if any(movie['id'] == data['id'] for movie in movies):
        return jsonify({"status": 400, "reason": "Фильм с таким ID уже существует"}), 400
    movies.append(data)
    return jsonify({"movie": data}), 200

# Маршрут для обновления информации о фильме по ID
@app.route('/api/movies/<int:id>', methods=['PATCH'])
def patch_movie(id):
    data = request.json.get('movie', {})
    validation_error = validate(data)
    if validation_error:
        return jsonify({"status": 400, "reason": validation_error}), 400
    movie = next((movie for movie in movies if movie['id'] == id), None)
    if movie is None:
        abort(404)
    movie.update(data)
    return jsonify({"movie": movie}), 200

# Маршрут для удаления фильма по ID
@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = next((movie for movie in movies if movie['id'] == id), None)
    if movie is None:
        abort(404)
    movies.remove(movie)
    return '', 202

# Обработчик ошибки 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": 404, "reason": "Не найдено"}), 404

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": 500, "reason": str(error)}), 500

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
