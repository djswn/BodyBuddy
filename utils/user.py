# utils/user.py

def make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks, gender):
    """
    전달받은 사용자 정보를 딕셔너리로 반환하는 함수
    """
    user_info = {
        "name": name,
        "age": age,
        "height": height,
        "weight": weight,
        "body_fat": body_fat,
        "target_weight": target_weight,
        "diet_period_weeks": diet_period_weeks,
        "gender": gender
    }
    return user_info
