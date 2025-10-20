from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            static_folder='.',
            static_url_path='')
CORS(app)  # Разрешаем CORS для всех доменов

# Путь к файлу с данными пользователей
# Проверяем несколько возможных путей
POSSIBLE_PATHS = [
    os.path.join(os.path.dirname(__file__), 'users_data.json'),       # ./users_data.json (Mini App folder)
    os.path.join(os.path.dirname(__file__), '..', 'users_data.json'),  # ../users_data.json
    '/opt/render/project/src/users_data.json',                       # Render.com путь
    os.path.join(os.getcwd(), 'users_data.json'),                    # Текущая директория
]

USERS_DATA_FILE = None
for path in POSSIBLE_PATHS:
    if os.path.exists(path):
        USERS_DATA_FILE = path
        print(f"Found users_data.json at: {path}")
        break

if USERS_DATA_FILE is None:
    print(f"Warning: users_data.json not found in any of: {POSSIBLE_PATHS}")
    USERS_DATA_FILE = POSSIBLE_PATHS[0]  # Используем первый путь как fallback

@app.route('/api/user-profile', methods=['GET'])
def get_user_profile():
    """
    API endpoint для получения данных профиля пользователя
    Ожидает user_id в query параметрах
    """
    user_id = request.args.get('user_id')

    if not user_id:
        print(f"API Error: user_id parameter missing")
        return jsonify({'error': 'user_id is required'}), 400

    print(f"API Request: Getting profile for user_id {user_id}")

    try:
        # Загружаем данные пользователей
        if os.path.exists(USERS_DATA_FILE):
            with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            print(f"Users data loaded successfully, {len(users_data)} users found")
        else:
            print(f"API Error: users_data.json not found at {USERS_DATA_FILE}")
            return jsonify({'error': 'User data not found'}), 404

        # Ищем пользователя
        if user_id not in users_data:
            print(f"API Error: User {user_id} not found in users_data")
            print(f"Available users: {list(users_data.keys())}")
            return jsonify({'error': 'User not found'}), 404

        user_data = users_data[user_id]
        print(f"User data found: {user_data}")

        # Проверяем, что пользователь завершил настройку
        if not user_data.get('setup_completed', False):
            print(f"API Error: User {user_id} profile not completed")
            return jsonify({'error': 'User profile not completed'}), 403

        # Форматируем дату регистрации
        reg_date_raw = user_data.get('registration_date', 'Не указано')
        if reg_date_raw != 'Не указано' and str(reg_date_raw).isdigit():
            # Если это timestamp, конвертируем в дату
            import time
            reg_date = time.strftime('%Y-%m-%d', time.localtime(int(reg_date_raw)))
        else:
            reg_date = reg_date_raw

        # Формируем ответ с данными профиля
        profile_data = {
            'name': user_data.get('name', 'Не указано'),
            'username': user_data.get('username', ''),
            'age': user_data.get('age', 'Не указано'),
            'city': user_data.get('city', 'Не указано'),
            'registration_date': reg_date,
            'total_reports': user_data.get('total_reports', 0),
            'active_reports': user_data.get('active_reports', 0),
            'resolved_reports': user_data.get('resolved_reports', 0)
        }

        print(f"API Response: {profile_data}")
        return jsonify(profile_data)

    except Exception as e:
        print(f"API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Отдаем статический HTML файл"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Отдаем CSS файл"""
    return send_from_directory('.', 'styles.css')

@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug endpoint для проверки работы API"""
    debug_info = {
        'status': 'ok',
        'timestamp': '2024-01-01T00:00:00Z',
        'users_data_file': USERS_DATA_FILE,
        'file_exists': os.path.exists(USERS_DATA_FILE),
        'current_dir': os.getcwd(),
        'files_in_current_dir': os.listdir('.') if os.path.exists('.') else [],
        'parent_dir': os.path.dirname(__file__),
        'files_in_parent_dir': os.listdir(os.path.dirname(__file__)) if os.path.exists(os.path.dirname(__file__)) else []
    }

    if debug_info['file_exists']:
        try:
            with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            debug_info['users_count'] = len(users_data)
            debug_info['user_ids'] = list(users_data.keys())
        except Exception as e:
            debug_info['file_read_error'] = str(e)

    return jsonify(debug_info)

if __name__ == '__main__':
    # Получаем порт из переменной окружения (для Render.com)
    port = int(os.environ.get('PORT', 5000))
    # Слушаем на всех интерфейсах (для production)
    app.run(host='0.0.0.0', port=port, debug=False)