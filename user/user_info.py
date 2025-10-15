# 사용자 정보 입력
user_info = {}

user_info["name"] = input("이름: ")
user_info["age"] = int(input("나이: "))
user_info["height"] = float(input("신장(cm): "))
user_info["weight"] = float(input("체중(kg): "))
user_info["body_fat"] = float(input("체지방(%): "))
user_info["target_weight"] = float(input("목표 체중(kg): "))
user_info["diet_period_weeks"] = int(input("다이어트 기간(주 단위): "))

print("\n입력 완료! 사용자 정보:")
for key, value in user_info.items():
    print(f"{key}: {value}")
