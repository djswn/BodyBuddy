	def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def calculate_bmr(weight, height, age, gender):
    if gender == "남":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def recommended_calories(bmr, activity_factor=1.2):
    return bmr * activity_factor
