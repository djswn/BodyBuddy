def calculate_bmi(weight, height):
    """
    BMI 계산
    weight: 체중 (kg)
    height: 신장 (cm)
    """
    height_m = height / 100  # cm → m 변환
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def calculate_bmr(weight, height, age, gender):
    """
    BMR 계산 (Mifflin-St Jeor 공식)
    weight: 체중 (kg)
    height: 신장 (cm)
    age: 나이 (세)
    gender: 'male' 또는 'female'
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("gender는 'male' 또는 'female'이어야 합니다.")
    return round(bmr, 2)
