from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from datetime import datetime
import os
import json

bp = Blueprint('weights', __name__, template_folder='../templates', static_folder='../static')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'weights.json')

def ensure_datafile():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_weights():
    ensure_datafile()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_weights(data):
    ensure_datafile()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bp.route('/weights', methods=['GET'])
def show_weights():
    weights = load_weights()
    return render_template('weights.html', weights=weights)

@bp.route('/weights/add', methods=['POST'])
def add_weight():
    try:
        weight_raw = request.form.get('weight', '').strip()
        date_raw = request.form.get('date', '').strip()

        if not weight_raw:
            flash('체중을 입력하세요.', 'error')
            return redirect(url_for('weights.show_weights'))

        weight = float(weight_raw)
        if weight <= 0:
            flash('체중은 0보다 커야 합니다.', 'error')
            return redirect(url_for('weights.show_weights'))

        if date_raw:
            try:
                date_obj = datetime.strptime(date_raw, '%Y-%m-%d').date()
            except ValueError:
                flash('날짜 형식은 YYYY-MM-DD로 입력하세요.', 'error')
                return redirect(url_for('weights.show_weights'))
        else:
            date_obj = datetime.now().date()

        data = load_weights()
        date_str = date_obj.isoformat()
        replaced = False
        for item in data:
            if item.get('date') == date_str:
                item['weight'] = weight
                item['updated_at'] = datetime.now().isoformat()
                replaced = True
                break
        if not replaced:
            data.append({
                'date': date_str,
                'weight': weight,
                'created_at': datetime.now().isoformat()
            })

        data.sort(key=lambda x: x['date'])
        save_weights(data)
        flash('체중이 저장되었습니다.', 'success')
        return redirect(url_for('weights.show_weights'))

    except ValueError:
        flash('숫자 형식이 잘못되었습니다.', 'error')
        return redirect(url_for('weights.show_weights'))
    except Exception as e:
        current_app.logger.exception("체중 저장 중 오류")
        flash('서버 오류가 발생했습니다.', 'error')
        return redirect(url_for('weights.show_weights'))

@bp.route('/weights/data', methods=['GET'])
def weights_data():
    data = load_weights()
    labels = [item['date'] for item in data]
    values = [item['weight'] for item in data]
    return jsonify({'labels': labels, 'values': values, 'raw': data})
