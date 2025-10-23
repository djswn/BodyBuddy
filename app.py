from flask import Flask, render_template, request, redirect, url_for
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr
import datetime

app = Flask(__name__)

# 임시 저장소
users = {}
progress_data = []

# 첫 시작화면
@app.route('/')
def index():
    return render_template('index.html')

# 로그인
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        # TODO: 실제 인증 로직
        return redirect(url_for('userInfo'))
    return render_template('login.html')

# 사용자 정보 입력
@app.route('/userInfo', methods=['GET','POST'])
def userInfo():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        body_fat = float(request.form.get('body_fat', 0))
        target_weight = float(request.form['target_weight'])
        diet_period_weeks = int(request.form['diet_period'])

        user_info = make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks)
        users[name] = user_info

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        # 추천 식단/운동/멘트
        sample_meals = {
            "아침": "귀리 + 계란",
            "점심": "현미밥 + 닭가슴살",
            "저녁": "샐러드 + 연어"
        }
        sample_exercise = "30분 조깅"
        comment = "잘 하고 있어요!" if weight <= target_weight else "조심하세요, 체중이 늘고 있어요!"

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            meals=sample_meals,
            exercise=sample_exercise,
            comment=comment,
            weight=weight
        )
    return render_template('userInfo.html')

# 체중 증감 버튼
@app.route('/update_weight', methods=['POST'])
def update_weight():
    global progress_data
    action = request.form['action']
    current_weight = float(request.form['weight'])
    if action == 'plus':
        current_weight += 1
    elif action == 'minus':
        current_weight -= 1
    progress_data.append({"date": datetime.date.today().isoformat(), "weight": current_weight})

    bmi = calculate_bmi(current_weight, 170)  # 예시: 키 170cm
    bmr = calculate_bmr(current_weight, 170, 25, "male")

    sample_meals = {
        "아침": "귀리 + 계란",
        "점심": "현미밥 + 닭가슴살",
        "저녁": "샐러드 + 연어"
    }
    sample_exercise = "30분 조깅"
    comment = "잘 하고 있어요!" if current_weight <= 70 else "조심하세요, 체중이 늘고 있어요!"

    return render_template(
        'character&diet,exercise.html',
        user_info={"name": "사용자"},
        bmi=bmi,
        bmr=bmr,
        meals=sample_meals,
        exercise=sample_exercise,
        comment=comment,
        weight=current_weight
    )

if __name__ == '__main__':
    app.run(debug=True)
