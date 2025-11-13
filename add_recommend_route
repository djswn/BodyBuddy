@app.route('/recommend/<user_id>')
def recommend(user_id):
    meals = get_daily_meals()
    exercise = get_daily_exercise()
    return render_template(
        'recommend.html',
        meals=meals,
        exercise=exercise,
        user_id=user_id
    )
