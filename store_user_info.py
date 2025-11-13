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

        user_info = make_user_info(
            name, age, height, weight, body_fat,
            target_weight, diet_period_weeks, gender
        )
        users[user_id]['info'] = user_info

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        meals = get_daily_meals()
        exercise = get_daily_exercise()
        comment = get_health_comment(weight, height, age, gender, bmr, target_weight)
        character_img = get_character_image(weight, height, age, gender, bmr)

        return render_template(
            'character&diet,exercise.html',
            user_info=user_info,
            bmi=bmi,
            bmr=bmr,
            meals=meals,
            exercise=exercise,
            comment=comment,
            weight=weight,
            user_id=user_id,
            character_img=character_img
        )
    else:
        # GET 요청 시 기존 사용자 정보 불러오기 -> 사용자 정보 수정 시, 마지막으로 저장했던 정보 표시
        user_info = users.get(user_id, {}).get('info')
        return render_template('userInfo.html', user_id=user_id, user_info=user_info)
