from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Путь к файлу с данными пользователей
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'users_data.json')

@app.route('/api/user-profile', methods=['GET'])
def get_user_profile():
    """
    API endpoint для получения данных профиля пользователя
    Ожидает user_id в query параметрах
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    try:
        # Загружаем данные пользователей
        if os.path.exists(USERS_DATA_FILE):
            with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
        else:
            return jsonify({'error': 'User data not found'}), 404

        # Ищем пользователя
        if user_id not in users_data:
            return jsonify({'error': 'User not found'}), 404

        user_data = users_data[user_id]

        # Проверяем, что пользователь завершил настройку
        if not user_data.get('setup_completed', False):
            return jsonify({'error': 'User profile not completed'}), 403

        # Формируем ответ с данными профиля
        profile_data = {
            'name': user_data.get('name', 'Не указано'),
            'username': user_data.get('username', ''),
            'age': user_data.get('age', 'Не указано'),
            'city': user_data.get('city', 'Не указано'),
            'registration_date': user_data.get('registration_date', 'Не указано'),
            'total_reports': user_data.get('total_reports', 0),
            'active_reports': user_data.get('active_reports', 0),
            'resolved_reports': user_data.get('resolved_reports', 0)
        }

        return jsonify(profile_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Отдаем статический HTML файл"""
    return app.send_static_file('index.html')

@app.route('/styles.css')
def styles():
    """Отдаем CSS файл"""
    return app.send_static_file('styles.css')

if __name__ == '__main__':
    app.run(debug=True)