from flask import Flask, render_template, request, redirect, url_for
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr
import datetime
import json, os, random

app = Flask(__name__)

DATA_FILE = "users.json"

# 기존 데이터 불러오기
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

# -------------------------------
# 식단/운동 데이터 풀
# -------------------------------
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

# -------------------------------
# AI 멘트 로직
# -------------------------------
def get_health_comment(weight, height, bmr, target_weight):
    bmi = calculate_bmi(weight, height)
    if bmi < 18.5:
        return "현재 저체중 상태예요. 건강을 위해 체중을 조금 늘리는 게 좋아요."
    elif 18.5 <= bmi < 23:
        return "정상 체중이에요! 지금처럼 꾸준히 관리해보세요."
    elif 23 <= bmi < 25:
        return "과체중 상태예요. 식단과 운동을 조금 더 신경쓰면 좋아요."
    else:
        return "비만 상태예요. 건강을 위해 적극적인 관리가 필요해요."

# -------------------------------
# 라우트
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = users.get(user_id)
        if not user or user['password'] != password:
            return "아이디 또는 비밀번호가 잘못되었습니다."

        if user['info']:
            user_info = user['info']
            gender = user_info.get('gender', 'male')  # 안전 접근
            bmi = calculate_bmi(user_info['weight'], user_info['height'])
            bmr = calculate_bmr(user_info['weight'], user_info['height'], user_info['age'], gender)

            meals = get_daily_meals()
            exercise = get_daily_exercise()
            comment = get_health_comment(user_info['weight'], user_info['height'], bmr, user_info['target_weight'])

            return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
                meals=meals,
                exercise=exercise,
                comment=comment,
                weight=user_info['weight'],
                user_id=user_id
            )
        else:
            return redirect(url_for('userInfo', user_id=user_id))

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users:
            return "이미 존재하는 아이디입니다."

        users[user_id] = {"password": password, "info": None}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        return redirect(url_for('userInfo', user_id=user_id))

    return render_template('register.html')

@app.route('/userInfo/<user_id>', methods=['GET','POST'])
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

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        meals = get_daily_meals()
        exercise = get_daily_exercise()
        comment = get_health_comment(weight, height, bmr, target_weight)

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            meals=meals,
            exercise=exercise,
            comment=comment,
            weight=weight,
            user_id=user_id
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
        current_weight += 1
    elif action == 'minus':
        current_weight -= 1

    # 사용자 정보 업데이트
    users[user_id]['info']['weight'] = current_weight
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    user_info = users[user_id]['info']
    gender = user_info.get('gender', 'male')  # 안전 접근
    bmi = calculate_bmi(current_weight, user_info['height'])
    bmr = calculate_bmr(current_weight, user_info['height'], user_info['age'], gender)
    comment = get_health_comment(current_weight, user_info['height'], bmr, user_info['target_weight'])

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
        user_id=user_id
    )

if __name__ == '__main__':
    app.run(debug=True)