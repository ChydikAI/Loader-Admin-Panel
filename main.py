from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'randomsecretkey1234'
db = SQLAlchemy(app)


# Модели данных
class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey('key.id'), nullable=False)
    processor = db.Column(db.String(128))
    motherboard = db.Column(db.String(128))
    bios_version = db.Column(db.String(128))
    bios_date = db.Column(db.String(64))
    disk = db.Column(db.String(128))
    gpu = db.Column(db.String(128))
    ram = db.Column(db.String(64))
    monitor = db.Column(db.String(128))
    os_name = db.Column(db.String(128))
    arch = db.Column(db.String(64))
    mac_address = db.Column(db.String(64))
    ip = db.Column(db.String(15))


class KeyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey('key.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(15))
    status = db.Column(db.String(64))


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, nullable=False)
    hwid = db.Column(db.String(64), nullable=True)
    ip = db.Column(db.String(15), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_frozen = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    is_bsod = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    system_info = db.relationship('SystemInfo', backref='key', uselist=False)
    logs = db.relationship('KeyLog', backref='key', lazy=True)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loader_version = db.Column(db.String(16), nullable=False, default="1.0.0")



with app.app_context():
    db.create_all()
    if not Settings.query.first():
        db.session.add(Settings(loader_version="1.0.0"))
        db.session.commit()



def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))



@app.route('/api/keys', methods=['POST'])
def create_key():
    try:
        duration_str = request.json.get('duration')
        if not duration_str:
            return jsonify({"error": "Не указана длительность"}), 400

        if duration_str == "LifeTime":
            expires_at = datetime.utcnow() + timedelta(days=999999)
        else:
            duration_map = {
                "minutes": timedelta(minutes=1),
                "hours": timedelta(hours=1),
                "days": timedelta(days=1)
            }
            value, unit = duration_str.split()
            value = int(value)
            expires_at = datetime.utcnow() + (value * duration_map[unit])

        new_key = Key(
            key=generate_key(),
            expires_at=expires_at
        )
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'key': new_key.key, 'expires_at': expires_at.isoformat()}), 201
    except Exception as e:
        return jsonify({"error": f"Ошибка при создании ключа: {str(e)}"}), 500


@app.route('/api/keys', methods=['GET'])
def get_all_keys():
    try:
        keys = Key.query.all()
        key_data = [{
            "id": key.id,
            "key": key.key,
            "expires_at": key.expires_at,
            "is_frozen": key.is_frozen,
            "is_banned": key.is_banned,
            "is_bsod": key.is_bsod,
            "created_at": key.created_at
        } for key in keys]

        return jsonify(key_data), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при получении ключей: {str(e)}"}), 500


# Роут для получения информации о ключе
@app.route('/api/keys/<string:key_str>', methods=['GET'])
def get_key_info(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    key_info = {
        'key': key.key,
        'expires_at': key.expires_at.isoformat(),
        'is_frozen': key.is_frozen,
        'is_banned': key.is_banned,
        'is_bsod': key.is_bsod,
        'hwid': key.hwid,
        'created_at': key.created_at.isoformat(),
    }
    return jsonify(key_info)



@app.route('/api/keys/<string:key_str>/auth_history', methods=['GET'])
def get_auth_history(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    logs = KeyLog.query.filter_by(key_id=key.id).all()
    return jsonify([{
        'timestamp': log.timestamp.isoformat(),
        'ip': log.ip,
        'status': log.status
    } for log in logs])


# Роут для обновления версии лоадера
@app.route('/api/settings/loader_version', methods=['PUT'])
def update_loader_version():
    try:
        loader_version = request.json.get('loader_version')
        if not loader_version:
            return jsonify({"error": "Не указана версия лоадера"}), 400

        settings = Settings.query.first()
        settings.loader_version = loader_version
        db.session.commit()
        return jsonify({'message': 'Версия лоадера обновлена'}), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при обновлении версии лоадера: {str(e)}"}), 500


# Роут для валидации ключа
@app.route('/api/validate', methods=['POST'])
def validate_key():
    required_fields = ['key', 'hwid', 'system_info', 'loader_version']
    system_info_fields = [
        'processor', 'motherboard', 'bios_version', 'bios_date', 'disk',
        'gpu', 'ram', 'monitor', 'os_name', 'arch', 'mac_address', 'ip'
    ]

    try:
        data = request.json
        if not data:
            return jsonify({"valid": False, "error": "Данные запроса отсутствуют"}), 400
        print(f"Получены данные: {data}")

        for field in required_fields:
            if field not in data:
                return jsonify({"valid": False, "error": f"Отсутствует поле {field}"}), 400

        system_info_data = data.get('system_info', {})
        for field in system_info_fields:
            if field not in system_info_data:
                return jsonify({"valid": False, "error": f"Отсутствует поле system_info.{field}"}), 400

        key_str = data['key']
        hwid = data['hwid']
        loader_version = data['loader_version']

        settings = Settings.query.first()
        if settings and loader_version != settings.loader_version:
            return jsonify({"valid": False, "error": "Неподдерживаемая версия лоадера"}), 400

        key = Key.query.filter_by(key=key_str).first()
        if not key:
            return jsonify({"valid": False, "error": "Ключ недействителен"}), 400

        if key.is_banned:
            return jsonify({"valid": False, "error": "Ключ заблокирован"}), 400

        if key.is_bsod:
            return jsonify({"bsod": True}), 400

        if key.is_frozen:
            return jsonify({"valid": False, "error": "Ключ заморожен"}), 400

        if key.expires_at and key.expires_at < datetime.utcnow():
            return jsonify({"valid": False, "error": "Ключ истёк"}), 400

        if key.hwid and key.hwid != hwid:
            return jsonify({"valid": False, "error": "HWID не совпадает"}), 400

        if not key.hwid:
            key.hwid = hwid
            key.ip = system_info_data.get('ip', '0.0.0.0')
            db.session.commit()

        system_info = key.system_info or SystemInfo(key_id=key.id)
        system_info.processor = system_info_data['processor']
        system_info.motherboard = system_info_data['motherboard']
        system_info.bios_version = system_info_data['bios_version']
        system_info.bios_date = system_info_data['bios_date']
        system_info.disk = system_info_data['disk']
        system_info.gpu = system_info_data['gpu']
        system_info.ram = system_info_data['ram']
        system_info.monitor = system_info_data['monitor']
        system_info.os_name = system_info_data['os_name']
        system_info.arch = system_info_data['arch']
        system_info.mac_address = system_info_data['mac_address']
        system_info.ip = system_info_data['ip']
        db.session.add(system_info)
        db.session.commit()

        log = KeyLog(key_id=key.id, ip=system_info.ip, status="Успешно")
        db.session.add(log)
        db.session.commit()

        return jsonify({"valid": True, "message": "Ключ активен"}), 200

    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")  # Логирование ошибки
        return jsonify({"valid": False, "error": f"Ошибка обработки запроса: {str(e)}"}), 500




@app.route('/api/keys/<string:key_str>/freeze', methods=['POST'])
def toggle_freeze_key(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    key.is_frozen = not key.is_frozen
    db.session.commit()
    return jsonify({"message": f"Статус заморозки изменён на {key.is_frozen}"}), 200



@app.route('/api/keys/<string:key_str>/ban', methods=['POST'])
def toggle_ban_key(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    key.is_banned = not key.is_banned
    db.session.commit()
    return jsonify({"message": f"Статус блокировки изменён на {key.is_banned}"}), 200



@app.route('/api/keys/<string:key_str>/reset_hwid', methods=['POST'])
def reset_hwid(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    key.hwid = None
    db.session.commit()
    return jsonify({"message": "HWID сброшен"}), 200



@app.route('/api/keys/<string:key_str>/add_time', methods=['POST'])
def add_time(key_str):
    key = Key.query.filter_by(key=key_str).first()
    if not key:
        return jsonify({"error": "Ключ не найден"}), 404

    days = request.json.get('days', 0)
    if days <= 0:
        return jsonify({"error": "Не указано количество дней"}), 400

    key.expires_at += timedelta(days=days)
    db.session.commit()
    return jsonify({"message": f"Время добавлено, новый срок: {key.expires_at.isoformat()}"}), 200


@app.route('/api/key/<int:key_id>/system_info', methods=['GET'])
def get_system_info(key_id):
    try:

        key = Key.query.get_or_404(key_id)


        system_info = key.system_info
        if not system_info:
            return jsonify({"error": "Системная информация для этого ключа отсутствует"}), 404

        # Формируем ответ
        system_info_data = {
            "processor": system_info.processor,
            "motherboard": system_info.motherboard,
            "bios_version": system_info.bios_version,
            "bios_date": system_info.bios_date,
            "disk": system_info.disk,
            "gpu": system_info.gpu,
            "ram": system_info.ram,
            "monitor": system_info.monitor,
            "os_name": system_info.os_name,
            "arch": system_info.arch,
            "mac_address": system_info.mac_address,
            "ip": system_info.ip
        }

        return jsonify(system_info_data), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при получении системной информации: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
