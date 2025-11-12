from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr
import datetime
import json, os, random

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATA_FILE = "users.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

MEAL_PLANS = {
    "아침": ["귀리 + 계란", "고구마 100g + 닭가슴살 100g", "삶은 계란 2개 + 바나나 1개", "현미밥 100g + 두부구이"],
    "점심": ["현미밥 150g + 닭가슴살 100g + 채소류 100g", "잡곡밥 + 연어구이 + 샐러드", "곤약밥 + 소고기불고기 + 나물", "현미밥 + 두부조림 + 김치"],
    "저녁": ["샐러드 + 연어", "고구마 100g + 닭가슴살 100g", "두부스테이크 + 채소볶음", "현미밥 + 계란말이 + 나물"],
    "간식": ["고구마 50g", "삶은 계란 1개", "그릭요거트 + 견과류", "바나나 1개"]
}

EXERCISES = ["30분 조깅", "자전거 타기 40분", "홈트 HIIT 20분", "요가 30분", "수영 1시간", "줄넘기 1000개"]


def get_daily_meals():
    today = datetime.date.today()
    random.seed(today.toordinal())
    return {meal: random.choice(options) for meal, options in MEAL_PLANS.items()}


def get_daily_exercise():
    today = datetime.date.today()
    random.seed(today.toordinal() + 999)
    return random.choice(EXERCISES)


def get_health_comment(weight, height, age, gender, bmr, target_weight):
    bmi = calculate_bmi(weight, height)

    if bmi < 18.5:
        return "현재 저체중 상태예요. 영양을 충분히 섭취하고 근육량을 늘리는 게 좋아요."
    elif 18.5 <= bmi < 23:
        if gender == 'female' and age >= 35 and bmr < 1400:
            return "체중은 정상 범위지만, 대사량이 낮아 지방 축적 위험이 있어요. 규칙적인 운동으로 근육량을 늘려보세요."
        else:
            return "정상 체중이에요! 지금처럼 균형 잡힌 식단과 운동을 유지해보세요."
    elif 23 <= bmi < 25:
        if gender == 'male' and bmr < 1500:
            return "과체중 상태이며, 대사량이 낮아 체중 관리에 더 신경 써야 해요. 유산소와 근력 운동을 병행해보세요."
        else:
            return "과체중 상태예요. 식단 조절과 함께 활동량을 늘리면 건강 개선에 도움이 돼요."
    else:
        if age >= 40 and bmr < 1400:
            return "비만 상태이며, 나이와 대사량을 고려했을 때 건강 위험이 커요. 전문가 상담과 함께 체계적인 관리가 필요해요."
        else:
            return "비만 상태예요. 식단과 운동을 적극적으로 관리해 건강을 지켜주세요."


def get_character_image(weight, height, age, gender, bmr):
    bmi = calculate_bmi(weight, height)

    if bmi < 18.5:
        return url_for('static', filename='images/gonyani.jpeg')
    elif 18.5 <= bmi < 23:
        if gender == 'female' and age >= 35 and bmr < 1400:
            return url_for('static', filename='images/fat_gonyani.png')
        else:
            return url_for('static', filename='images/gonyani.jpeg')
    else:
        return url_for('static', filename='images/fat_gonyani.png')


# 새로 추가: 체중 기록 저장 함수
def save_weight_record(user_id, weight):
    """날짜별 체중 기록 저장"""
    today = datetime.date.today().isoformat()

    if 'weight_history' not in users[user_id]:
        users[user_id]['weight_history'] = []

    # 오늘 날짜 기록이 있으면 업데이트, 없으면 추가
    history = users[user_id]['weight_history']
    updated = False
    for record in history:
        if record['date'] == today:
            record['weight'] = weight
            updated = True
            break

    if not updated:
        history.append({'date': today, 'weight': weight})

    # 날짜순 정렬
    users[user_id]['weight_history'].sort(key=lambda x: x['date'])

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = users.get(user_id)
        if not user or user['password'] != password:
            return "아이디 또는 비밀번호가 잘못되었습니다."

        if user['info']:
            user_info = user['info']
            gender = user_info.get('gender', 'male')
            bmi = calculate_bmi(user_info['weight'], user_info['height'])
            bmr = calculate_bmr(user_info['weight'], user_info['height'], user_info['age'], gender)

            meals = get_daily_meals()
            exercise = get_daily_exercise()
            comment = get_health_comment(user_info['weight'], user_info['height'], user_info['age'], gender, bmr,
                                         user_info['target_weight'])
            character_img = get_character_image(user_info['weight'], user_info['height'], user_info['age'], gender, bmr)

            return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
                meals=meals,
                exercise=exercise,
                comment=comment,
                weight=user_info['weight'],
                user_id=user_id,
                character_img=character_img
            )
        else:
            return redirect(url_for('userInfo', user_id=user_id))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users:
            return "이미 존재하는 아이디입니다."

        users[user_id] = {"password": password, "info": None, "weight_history": []}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        return redirect(url_for('userInfo', user_id=user_id))

    return render_template('register.html')


@app.route('/userInfo/<user_id>', methods=['GET', 'POST'])
def userInfo(user_id):
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        body_fat = float(request.form.get('body_fat', 0))
        target_weight = float(request.form['target_weight'])
        diet_period_weeks = int(request.form['diet_period'])

        user_info = make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks, gender)
        users[user_id]['info'] = user_info

        # 초기 체중 기록
        save_weight_record(user_id, weight)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        meals = get_daily_meals()
        exercise = get_daily_exercise()
        comment = get_health_comment(weight, height, age, gender, bmr, target_weight)
        character_img = get_character_image(weight, height, age, gender, bmr)

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            meals=meals,
            exercise=exercise,
            comment=comment,
            weight=weight,
            user_id=user_id,
            character_img=character_img
        )
    return render_template('userInfo.html', user_id=user_id)


@app.route('/update_weight', methods=['POST'])
def update_weight():
    user_id = request.form.get('user_id')
    if not user_id or user_id not in users or not users[user_id].get('info'):
        return "사용자 정보가 없습니다. 다시 로그인해주세요."

    action = request.form['action']
    current_weight = float(request.form['weight'])

    if action == 'plus':
        current_weight += 0.5
    elif action == 'minus':
        current_weight -= 0.5

    users[user_id]['info']['weight'] = current_weight

    # 체중 변경 시 기록 저장
    save_weight_record(user_id, current_weight)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    user_info = users[user_id]['info']
    gender = user_info.get('gender', 'male')
    bmi = calculate_bmi(current_weight, user_info['height'])
    bmr = calculate_bmr(current_weight, user_info['height'], user_info['age'], gender)

    comment = get_health_comment(
        current_weight,
        user_info['height'],
        user_info['age'],
        gender,
        bmr,
        user_info['target_weight']
    )
    character_img = get_character_image(current_weight, user_info['height'], user_info['age'], gender, bmr)

    meals = get_daily_meals()
    exercise = get_daily_exercise()

    return render_template(
        'character&diet,exercise.html',
        user_info=user_info,
        bmi=bmi,
        bmr=bmr,
        meals=meals,
        exercise=exercise,
        comment=comment,
        weight=current_weight,
        user_id=user_id,
        character_img=character_img
    )


# 새로 추가: 그래프 페이지
@app.route('/weight_graph/<user_id>')
def weight_graph(user_id):
    if user_id not in users or not users[user_id].get('info'):
        return redirect(url_for('login'))

    user_info = users[user_id]['info']
    return render_template('weight_graph.html', user_id=user_id, user_info=user_info)


# 새로 추가: 그래프 데이터 API
@app.route('/api/weight_data/<user_id>')
def weight_data(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    weight_history = users[user_id].get('weight_history', [])
    target_weight = users[user_id].get('info', {}).get('target_weight', None)

    return jsonify({
        'history': weight_history,
        'target_weight': target_weight
    })


if __name__ == '__main__':
    app.run(debug=True)