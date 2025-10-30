@app.route('/userInfo/<user_id>', methods=['GET','POST'])
def userInfo(user_id):
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        body_fat = float(request.form.get('body_fat', 0))
        target_weight = float(request.form['target_weight'])
        diet_period_weeks = int(request.form['diet_period'])

        user_info = make_user_info(name, age, height, weight, body_fat, target_weight, diet_period_weeks)
        users[user_id]['info'] = user_info  # 계정에 저장

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        sample_meals = {
            "아침": "귀리 + 계란",
            "점심": "현미밥 + 닭가슴살",
            "저녁": "샐러드 + 연어"
        }
        sample_exercise = "30분 조깅"
        comment = "잘 하고 있어요!" if weight <= target_weight else "조심하세요, 체중이 늘고 있어요!"

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            meals=sample_meals,
            exercise=sample_exercise,
            comment=comment,
            weight=weight
        )
    return render_template('userInfo.html', user_id=user_id)
