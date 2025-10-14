from flask import Flask, render_template, request
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr

app = Flask(__name__)

# 첫 시작화면
@app.route('/')
def index():
    return render_template('index.html')

# 메인 페이지
@app.route('/home')
def home():
    return render_template('home.html')

# 로그인
@app.route('/login')
def login():
    return render_template('login.html')

# 사용자 정보 입력
@app.route('/userInfo')
def userInfo():
    return render_template('userInfo.html')

# 📌 결과 페이지 라우트
@app.route('/result', methods=['POST'])
def result():
    # HTML 폼에서 값 받기
    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    body_fat = float(request.form.get('body_fat', 0.0))  # 체지방률이 없으면 0.0으로 설정

    # 아직 안 받는 값은 기본값 처리
    target_weight = weight
    diet_period_weeks = 0

    # user.py 함수 사용
    user_info = make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks)

    # BMI, BMR 계산
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)

    # 결과 페이지로 전달
    return render_template(
        'result.html',
        user_info=user_info,
        bmi=bmi,
        bmr=bmr
    )


if __name__ == '__main__':
    app.run(debug=True)
