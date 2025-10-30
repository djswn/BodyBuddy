from flask import Flask, render_template, request
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr
from utils.diet_recommender import get_diet_recommendation

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

# 식단 추천 페이지
@app.route('/recommand')
def recommand():
    # 기본값으로 처리 (실제로는 세션이나 쿠키 사용 권장)
    default_user_info = {
        'name': '사용자',
        'weight': 70,
        'height': 170,
        'age': 30,
        'target_weight': 65,
        'body_fat': 15
    }
    bmi = calculate_bmi(default_user_info['weight'], default_user_info['height'])
    bmr = calculate_bmr(default_user_info['weight'], default_user_info['height'], default_user_info['age'], 'male')
    diet_recommendation = get_diet_recommendation(default_user_info, bmi, bmr)
    
    return render_template('recommand.html', 
                         user_info=default_user_info,
                         bmi=bmi,
                         bmr=bmr,
                         **diet_recommendation)

# 식단 추천 결과 페이지
@app.route('/recommand_result', methods=['POST'])
def recommand_result():
    # HTML 폼에서 값 받기
    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    body_fat = float(request.form.get('body_fat', 0.0))
    target_weight = float(request.form.get('target_weight', weight))

    # user.py 함수 사용
    user_info = make_user_info(name, age, height, weight, body_fat, target_weight, 0)

    # BMI, BMR 계산
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)

    # 식단 추천
    diet_recommendation = get_diet_recommendation(user_info, bmi, bmr)

    # 식단 추천 페이지로 전달
    return render_template(
        'recommand.html',
        user_info=user_info,
        bmi=bmi,
        bmr=bmr,
        **diet_recommendation
    )

# 전역으로 임시 user_info 저장 (실제론 세션이나 DB 권장)
user_info_global = {
    'name': '사용자',
    'age': 30,
    'height': 170,
    'weight': 70,
    'body_fat': 15,
    'target_weight': 65,
    'diet_period_weeks': 0,
}

@app.route('/user_edit', methods=['GET', 'POST'])
def user_edit():
    global user_info_global
    if request.method == 'POST':
        # 폼 값 받아서 저장
        user_info_global['name'] = request.form['name']
        user_info_global['age'] = int(request.form['age'])
        user_info_global['height'] = float(request.form['height'])
        user_info_global['weight'] = float(request.form['weight'])
        user_info_global['body_fat'] = float(request.form.get('body_fat', 0.0))
        user_info_global['target_weight'] = float(request.form.get('target_weight', user_info_global['weight']))
        return render_template('home.html')
    # GET: 폼에 현재 값 전달
    return render_template('user_edit.html', user_info=user_info_global)


if __name__ == '__main__':
    app.run(debug=True)