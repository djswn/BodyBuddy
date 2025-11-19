# 드롭다운 음식 메뉴 (추가할 부분은 여기에)
FOODS = {
    "사과 1개": 200,
    "삶은 계란 1개": 250,
    "고구마 100g": 180,
    "바나나 1개": 150,
    "현미밥 100g": 130
}
=================================
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
