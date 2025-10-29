def recommend_meal_and_exercise(gender, nationality):
    meals = {
        "한국": ["닭가슴살 샐러드", "현미밥과 채소", "두부 스테이크"],
        "미국": ["그릴드 치킨과 샐러드", "오트밀과 과일", "연어 스테이크"],
        "일본": ["연어덮밥", "미소된장국과 채소", "두부 샐러드"]}
   
    exercises = ["오늘은 걷기 30분", "오늘은 가벼운 조깅", "오늘은 홈트 20분", "오늘은 요가 15분", "오늘은 자전거 30분"]

    meal = random.choice(meals.get(nationality, ["샐러드", "과일", "현미밥"]))
    exercise = random.choice(exercises)
   
    return meal, exercise
