# utils/diet_recommender.py

def get_diet_recommendation(user_info, bmi, bmr):
    """
    사용자 정보를 바탕으로 맞춤 식단을 추천하는 함수
    
    Args:
        user_info: 사용자 정보 딕셔너리
        bmi: BMI 값
        bmr: 기초대사율
    
    Returns:
        dict: 식단 추천 정보
    """
    
    # 목표 체중과 현재 체중 비교
    weight_diff = user_info['target_weight'] - user_info['weight']
    
    # BMI 기준으로 체형 분류
    if bmi < 18.5:
        body_type = "저체중"
        diet_type = "체중 증가 식단"
        diet_description = "건강한 체중 증가를 위한 고칼로리, 고단백 식단을 추천합니다."
        calorie_adjustment = 500  # 칼로리 증가
    elif bmi < 23:
        body_type = "정상체중"
        if weight_diff > 0:
            diet_type = "체중 증가 식단"
            diet_description = "건강한 체중 증가를 위한 균형잡힌 식단을 추천합니다."
            calorie_adjustment = 300
        else:
            diet_type = "유지 식단"
            diet_description = "현재 체중을 유지하기 위한 균형잡힌 식단을 추천합니다."
            calorie_adjustment = 0
    elif bmi < 25:
        body_type = "과체중"
        diet_type = "체중 감소 식단"
        diet_description = "건강한 체중 감소를 위한 저칼로리, 고단백 식단을 추천합니다."
        calorie_adjustment = -300
    else:
        body_type = "비만"
        diet_type = "체중 감소 식단"
        diet_description = "효과적인 체중 감소를 위한 저칼로리, 고단백 식단을 추천합니다."
        calorie_adjustment = -500
    
    # 권장 일일 칼로리 계산
    recommended_calories = int(bmr * 1.4 + calorie_adjustment)  # 활동대사율 1.4 적용
    
    # 식단 구성
    breakfast_calories = int(recommended_calories * 0.25)
    lunch_calories = int(recommended_calories * 0.35)
    dinner_calories = int(recommended_calories * 0.30)
    snack_calories = int(recommended_calories * 0.10)
    
    # 아침 식단
    breakfast = get_breakfast_menu(breakfast_calories, body_type)
    
    # 점심 식단
    lunch = get_lunch_menu(lunch_calories, body_type)
    
    # 저녁 식단
    dinner = get_dinner_menu(dinner_calories, body_type)
    
    # 간식
    snacks = get_snack_menu(snack_calories, body_type)
    
    # 식단 팁
    diet_tips = get_diet_tips(body_type, diet_type)
    
    return {
        'diet_type': diet_type,
        'diet_description': diet_description,
        'recommended_calories': recommended_calories,
        'breakfast_calories': breakfast_calories,
        'lunch_calories': lunch_calories,
        'dinner_calories': dinner_calories,
        'snack_calories': snack_calories,
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
        'diet_tips': diet_tips
    }

def get_breakfast_menu(calories, body_type):
    """아침 식단 메뉴 생성"""
    if body_type == "저체중":
        return [
            {"name": "현미밥 (1공기)", "calories": 200},
            {"name": "계란후라이 (2개)", "calories": 180},
            {"name": "아보카도 (1/2개)", "calories": 120},
            {"name": "우유 (1컵)", "calories": 150},
            {"name": "바나나 (1개)", "calories": 100}
        ]
    elif body_type in ["정상체중", "과체중", "비만"]:
        return [
            {"name": "현미밥 (1/2공기)", "calories": 100},
            {"name": "계란찜 (1개)", "calories": 90},
            {"name": "시금치나물", "calories": 30},
            {"name": "두부 (1/2모)", "calories": 80},
            {"name": "사과 (1/2개)", "calories": 50}
        ]

def get_lunch_menu(calories, body_type):
    """점심 식단 메뉴 생성"""
    if body_type == "저체중":
        return [
            {"name": "현미밥 (1.5공기)", "calories": 300},
            {"name": "닭가슴살 구이 (150g)", "calories": 200},
            {"name": "김치", "calories": 20},
            {"name": "미역국", "calories": 30},
            {"name": "브로콜리 (100g)", "calories": 40}
        ]
    elif body_type in ["정상체중", "과체중", "비만"]:
        return [
            {"name": "현미밥 (1공기)", "calories": 200},
            {"name": "닭가슴살 샐러드 (100g)", "calories": 120},
            {"name": "김치", "calories": 15},
            {"name": "된장국", "calories": 25},
            {"name": "시금치나물", "calories": 30}
        ]

def get_dinner_menu(calories, body_type):
    """저녁 식단 메뉴 생성"""
    if body_type == "저체중":
        return [
            {"name": "현미밥 (1공기)", "calories": 200},
            {"name": "연어구이 (120g)", "calories": 180},
            {"name": "콩나물국", "calories": 30},
            {"name": "오이무침", "calories": 20},
            {"name": "요거트 (1컵)", "calories": 100}
        ]
    elif body_type in ["정상체중", "과체중", "비만"]:
        return [
            {"name": "현미밥 (1/2공기)", "calories": 100},
            {"name": "연어구이 (80g)", "calories": 120},
            {"name": "미역국", "calories": 25},
            {"name": "오이무침", "calories": 15},
            {"name": "요거트 (1/2컵)", "calories": 50}
        ]

def get_snack_menu(calories, body_type):
    """간식 메뉴 생성"""
    if body_type == "저체중":
        return [
            {"name": "견과류 (30g)", "calories": 180},
            {"name": "바나나 (1개)", "calories": 100},
            {"name": "우유 (1컵)", "calories": 150}
        ]
    elif body_type in ["정상체중", "과체중", "비만"]:
        return [
            {"name": "견과류 (15g)", "calories": 90},
            {"name": "사과 (1/2개)", "calories": 50},
            {"name": "요거트 (1/2컵)", "calories": 50}
        ]

def get_diet_tips(body_type, diet_type):
    """체형과 식단 유형에 따른 팁 제공"""
    tips = []
    
    if body_type == "저체중":
        tips.extend([
            "규칙적인 식사 시간을 지켜주세요",
            "단백질과 탄수화물을 균형있게 섭취하세요",
            "간식을 통해 칼로리를 보충하세요",
            "충분한 수분 섭취를 유지하세요"
        ])
    elif body_type in ["과체중", "비만"]:
        tips.extend([
            "식사 전 물을 충분히 마시세요",
            "천천히 꼭꼭 씹어서 드세요",
            "야채를 먼저 드시고 주식을 드세요",
            "규칙적인 운동과 함께 식단을 지켜주세요"
        ])
    else:  # 정상체중
        tips.extend([
            "현재 체중을 유지하기 위해 균형잡힌 식사를 하세요",
            "규칙적인 식사 시간을 지켜주세요",
            "다양한 영양소를 골고루 섭취하세요",
            "충분한 수분 섭취를 유지하세요"
        ])
    
    return tips
