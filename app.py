from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.user import make_user_info
from utils.bmi_bmr import calculate_bmi, calculate_bmr
import datetime
import json, os, random

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATA_FILE = "users.json"

# 기존 데이터 불러오기
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}

# 드롭다운 음식 메뉴 (추가할 부분은 여기에)
FOODS = {
    "🥗 과일 / 채소": {
        "사과 1개": 95,
        "바나나 1개": 105,
        "오렌지 1개": 62,
        "방울토마토 10개": 30,
        "아보카도 1/2개": 120,
        "블루베리 100g": 57,
        "딸기 100g": 33,
        "오이 1개": 16,
        "삶은 당근 100g": 35,
        "삶은 브로콜리 100g": 55,
        "샐러리 100g": 14,
        "시금치 100g": 23,
        "양배추 100g": 25,
        "파프리카 1개": 45
    },

    "🍚 저칼로리 탄수화물": {
        "고구마 100g": 86,
        "현미밥 100g": 130,
        "오트밀 40g": 150,
        "잡곡밥 100g": 140,
        "옥수수 1개": 90,
        "통밀빵 1장": 70
    },

    "🍗 단백질": {
        "삶은 계란 1개": 70,
        "닭가슴살 100g": 110,
        "삶은 두부 100g": 80,
        "연어 100g": 142,
        "참치(물에 담긴) 100g": 116,
        "오징어 100g": 92,
        "삶은 새우 100g": 99,
        "그릭요거트 플레인 100g": 59,
        "저지방 우유 200ml": 90,
        "코티지치즈 100g": 98
    },

    "🥙 다이어트 식사 메뉴": {
        "시저샐러드(드레싱 적게) 1접시": 180,
        "닭가슴살 샐러드 1접시": 220,
        "연두부 샐러드 1접시": 160,
        "연어 샐러드 1접시": 250,
        "야채죽 1그릇": 120,
        "계란찜 1그릇": 150,
        "닭가슴살 샌드위치(통밀빵) 1개": 280
    },

    "🍪 건강 간식": {
        "아몬드 10개": 60,
        "호두 5개": 130,
        "건자두 5개": 110,
        "프로틴바 1개": 180,
        "현미떡 1개": 80,
        "팝콘(에어팝) 20g": 90
    }
}


# -------------------------------
# AI 멘트 로직
# -------------------------------
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

    if gender == 'male':
        if bmi < 18.5:
            # 저체중 남성 → 마른 가나디
            return url_for('static', filename='images/thin_ganadi.png')
        elif 18.5 <= bmi < 23:
            # 정상 남성 → 일반 가나디
            return url_for('static', filename='images/normal.png')
        else:
            # 과체중/비만 남성 → 뚱뚱한 가나디
            return url_for('static', filename='images/fat_ganadi.png')

    elif gender == 'female':
        if bmi < 18.5:
            # 저체중 여성 → 마른 고냐니
            return url_for('static', filename='images/underweight_gonyani.png')
        elif 18.5 <= bmi < 23:
            # 정상 여성 → 일반 고냐니
            return url_for('static', filename='images/gonyani.jpeg')
        else:
            # 과체중/비만 여성 → 뚱뚱한 고냐니
            return url_for('static', filename='images/fat_gonyani.png')

# 권장 칼로리 계산 함수: BMR * 활동 수준 계수(운동량에 따라 5단계로 나눔)

ACTIVITY_LEVELS = {
    "low": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "high": 1.725,
    "very_high": 1.9
}

def calculate_recommended_calories(weight, height, age, gender, activity_key="moderate"):
    bmr = calculate_bmr(weight, height, age, gender)
    activity_factor = ACTIVITY_LEVELS.get(activity_key, 1.55)  # 기본값: 보통 활동
    
    return round(bmr * activity_factor)

# -------------------------------
# 성취도 계산 함수
# -------------------------------
def calculate_progress(start_weight, current_weight, target_weight):
    if target_weight < start_weight:  # 감량 목표
        total_change = start_weight - target_weight
        current_change = start_weight - current_weight
    else:  # 증량 목표
        total_change = target_weight - start_weight
        current_change = current_weight - start_weight

    if total_change == 0:
        return 0
    if current_change < 0:
        return 0

    progress = float((current_change / total_change) * 100)
    return min(progress, 100)


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

# -------------------------------
# 라우트
# -------------------------------
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
            # 로그인 실패
            return render_template('login.html', error="아이디 또는 비밀번호가 잘못되었습니다.")

        if user['info']:
            user_info = user['info']
            gender = user_info.get('gender', 'male')
            bmi = calculate_bmi(user_info['weight'], user_info['height'])
            bmr = calculate_bmr(user_info['weight'], user_info['height'], user_info['age'], gender)

            # D-Day 계산
            start_date = datetime.datetime.strptime(user_info['start_date'], "%Y-%m-%d").date()
            total_days = user_info['diet_period_weeks'] * 7
            elapsed_days = (datetime.date.today() - start_date).days
            remaining_days = total_days - elapsed_days

            if remaining_days > 0:
                d_day_text = f"D-{remaining_days}"
                alarm_message = ""
            else:
                d_day_text = "D-Day"
                if user_info['weight'] <= user_info['target_weight']:
                    alarm_message = "성공했어요! 끝까지 해내다니 정말 멋있는데요?"
                else:
                    alarm_message = "아쉬워요! 다시 목표를 세워볼까요?"

            comment = get_health_comment(user_info['weight'], user_info['height'], user_info['age'], gender, bmr,
                                         user_info['target_weight'])
            character_img = get_character_image(user_info['weight'], user_info['height'], user_info['age'], gender, bmr)

            return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
                comment=comment,
                weight=user_info['weight'],
                user_id=user_id,
                character_img=character_img,
                d_day_text=d_day_text,
                alarm_message=alarm_message
            )
        else:
            return redirect(url_for('userInfo', user_id=user_id))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # 비밀번호 길이 체크
        if len(password) >= 9:
            return render_template('register.html', error="비밀번호는 반드시 8자리 이하여야 합니다.")

        if user_id in users:
            return render_template('register.html', error="이미 존재하는 아이디입니다.")

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
        start_weight = float(request.form.get('start_weight', weight))
        target_weight = float(request.form['target_weight'])
        diet_period_weeks = int(request.form['diet_period'])
        activity_level = request.form['activity_level']

        user_info = make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks, gender)
        user_info['start_weight'] = start_weight
        user_info['activity_level'] = request.form.get('activity_level', 'moderate')

        # 목표 기간 설정 이후 시작일 기록 (항상 오늘 날짜로 갱신)
        user_info['start_date'] = datetime.date.today().strftime("%Y-%m-%d")
        users[user_id]['info'] = user_info

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        comment = get_health_comment(weight, height, age, gender, bmr, target_weight)
        character_img = get_character_image(weight, height, age, gender, bmr)

        # D-Day 계산
        start_date = datetime.datetime.strptime(user_info['start_date'], "%Y-%m-%d").date()
        total_days = diet_period_weeks * 7
        elapsed_days = (datetime.date.today() - start_date).days
        remaining_days = total_days - elapsed_days

        if remaining_days > 0:
            d_day_text = f"D-{remaining_days}"
            alarm_message = ""
        else:
            d_day_text = "D-Day"
            if weight <= target_weight:
                alarm_message = "성공했어요! 끝까지 해내다니 정말 멋있는데요?"
            else:
                alarm_message = "아쉬워요! 다시 목표를 세워볼까요?"

        # 초기 체중 기록
        save_weight_record(user_id, weight)

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            comment=comment,
            weight=weight,
            user_id=user_id,
            character_img=character_img,
            d_day_text=d_day_text,
            alarm_message=alarm_message
        )
    else:
        user_info = users.get(user_id, {}).get('info')

        # start_date는 오늘 날짜로 초기화 
        if user_info and 'start_date' not in user_info:
            user_info['start_date'] = datetime.date.today().strftime("%Y-%m-%d")
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)

        return render_template('userInfo.html', user_id=user_id, user_info=user_info)

@app.route('/recommend/<user_id>')
def recommend(user_id):
    user_info = users[user_id]['info']

    recommended_calories = calculate_recommended_calories(
        user_info['weight'],
        user_info['height'],
        user_info['age'],
        user_info['gender'],
        user_info.get('activity_level', 'moderate')
    )

    start_weight = user_info.get('start_weight', user_info['weight'])
    progress = calculate_progress(start_weight, user_info['weight'], user_info['target_weight'])

    return render_template(
        'recommend.html',
        foods=FOODS,   
        user_id=user_id,
        user_name=user_info['name'],
        recommended_calories=recommended_calories,
        progress=progress
    )

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
    elif action == 'set':
        # 사용자가 직접 입력한 값 반영 (소수점 1자리까지)
        current_weight = round(current_weight, 1)

    # 사용자 체중 변경 업데이트
    users[user_id]['info']['weight'] = current_weight
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    # 사용자 정보 업데이트
    save_weight_record(user_id, current_weight)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    # BMI, BMR, 코멘트, 캐릭터 이미지 갱신
    user_info = users[user_id]['info']
    gender = user_info.get('gender', 'male')
    bmr = calculate_bmr(current_weight, user_info['height'], user_info['age'], gender)
    comment = get_health_comment(current_weight, user_info['height'], user_info['age'], gender, bmr, user_info['target_weight'])
    character_img = get_character_image(current_weight, user_info['height'], user_info['age'], gender, bmr)

    # 성취도 계산 추가
    start_weight = user_info.get('start_weight', current_weight)
    progress = calculate_progress(start_weight, current_weight, user_info['target_weight'])

    return {
        "weight": current_weight,
        "comment": comment,
        "character_img": character_img,
        "progress": progress
    }

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

@app.route('/logout')
def logout():
    session.clear()  # 세션 전체 초기화
    return redirect(url_for('index'))

# -------------------------------
# 앱 실행
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
