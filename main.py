from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = 'dasda12123adssd123adsasd123dsaESQWEQWASDASDASDAS1223EWDSAWD'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

@app.route('/update_loader_version', methods=['POST'])
def update_loader_version():
    try:
        loader_version = request.form.get('loader_version')
        if not loader_version:
            raise ValueError("Не указана версия лоадера")

        settings = Settings.query.first()
        settings.loader_version = loader_version
        db.session.commit()
        flash('Глобальная версия лоадера успешно обновлена!', 'success')
    except Exception as e:
        flash(f'Ошибка при обновлении версии лоадера: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/')
def admin_panel():
    keys = Key.query.all()
    now = datetime.utcnow()
    settings = Settings.query.first()
    return render_template('admin.html', keys=keys, now=now, format_date=format_date, settings=settings)


@app.route('/create', methods=['POST'])
def create_key():
    try:
        duration_str = request.form.get('duration')
        if not duration_str:
            raise ValueError("Не указана длительность")


        if duration_str == "LifeTime":
            expires_at = timedelta(days=999999)
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
        flash('Ключ успешно создан!', 'success')
    except Exception as e:
        flash(f'Ошибка при создании ключа: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/delete/<int:key_id>', methods=['POST'])
def delete_key(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        db.session.delete(key)
        db.session.commit()
        flash('Ключ успешно удален!', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении ключа: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/add_time/<int:key_id>', methods=['POST'])
def add_time(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        days = int(request.form.get('days', 0))
        key.expires_at += timedelta(days=days)
        db.session.commit()
        flash('Время успешно добавлено!', 'success')
    except Exception as e:
        flash(f'Ошибка при добавлении времени: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/freeze_key/<int:key_id>', methods=['POST'])
def freeze_key(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        key.is_frozen = not key.is_frozen
        db.session.commit()
        flash('Статус заморозки изменён!', 'success')
    except Exception as e:
        flash(f'Ошибка при изменении статуса: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/ban_key/<int:key_id>', methods=['POST'])
def ban_key(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        key.is_banned = not key.is_banned
        db.session.commit()
        flash('Статус блокировки изменён!', 'success')
    except Exception as e:
        flash(f'Ошибка при изменении блокировки: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/toggle_bsod/<int:key_id>', methods=['POST'])
def toggle_bsod(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        key.is_bsod = not key.is_bsod
        db.session.commit()
        flash('Статус BSOD изменён!', 'success')
    except Exception as e:
        flash(f'Ошибка при изменении BSOD: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/reset_hwid/<int:key_id>', methods=['POST'])
def reset_hwid(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        key.hwid = None
        db.session.commit()
        flash('HWID успешно сброшен!', 'success')
    except Exception as e:
        flash(f'Ошибка при сбросе HWID: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/validate', methods=['POST'])
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
        return jsonify({"valid": False, "error": f"Ошибка обработки запроса: {str(e)}"}), 500

@app.route('/auth_history/<int:key_id>', methods=['GET'])
def auth_history(key_id):
    logs = KeyLog.query.filter_by(key_id=key_id).all()
    return jsonify([{
        'timestamp': log.timestamp,
        'ip': log.ip,
        'status': log.status
    } for log in logs])

def format_date(date):
    now = datetime.utcnow()
    delta = now - date

    if date.date() == now.date():
        return f"Сегодня в {date.strftime('%H:%M')}"
    elif date.date() == (now - timedelta(days=1)).date():
        return f"Вчера в {date.strftime('%H:%M')}"
    elif 1 < delta.days <= 7:
        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        weekday = days_of_week[date.weekday()]
        return f"{weekday} в {date.strftime('%H:%M')}"
    elif now.year == date.year:
        return date.strftime('%d %B в %H:%M')
    else:
        return date.strftime('%d.%m.%Y в %H:%M')

if __name__ == '__main__':
    app.run(debug=True)
