@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = users.get(user_id)
        if not user or user['password'] != password:
            return "아이디 또는 비밀번호가 잘못되었습니다."

        if user['info']:
            user_info = user['info']

            if 'start_date' not in user_info:
                user_info['start_date'] = datetime.date.today().strftime("%Y-%m-%d")
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)

            gender = user_info.get('gender', 'male')
            bmi = calculate_bmi(user_info['weight'], user_info['height'])
            bmr = calculate_bmr(user_info['weight'], user_info['height'], user_info['age'], gender)

            # D-Day 계산
            start_date = datetime.datetime.strptime(user_info['start_date'], "%Y-%m-%d").date()
            total_days = user_info['diet_period_weeks'] * 7
            elapsed_days = (datetime.date.today() - start_date).days
            remaining_days = total_days - elapsed_days

            if remaining_days > 0:
                d_day_text = f"D-{remaining_days}"
                alarm_message = ""
            else:
                d_day_text = "D-Day"
                if user_info['weight'] <= user_info['target_weight']:
                    alarm_message = "성공했어요! 끝까지 해내다니 정말 멋있는데요?"
                else:
                    alarm_message = "아쉬워요! 다시 목표를 세워볼까요?"

            meals = get_daily_meals()
            exercise = get_daily_exercise()
            comment = get_health_comment(user_info['weight'], user_info['height'], user_info['age'], gender, bmr, user_info['target_weight'])
            character_img = get_character_image(user_info['weight'], user_info['height'], user_info['age'], gender, bmr)

            return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
                meals=meals,
                exercise=exercise,
                comment=comment,
                weight=user_info['weight'],
                user_id=user_id,
                character_img=character_img,
                d_day_text=d_day_text,
                alarm_message=alarm_message  
            )
        else:
            return redirect(url_for('userInfo', user_id=user_id))

    return render_template('login.html')
------------------------------------------------------------------------------------
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

        # 목표 기간 설정 이후 시작일 기록 (항상 오늘 날짜로 갱신)
        user_info['start_date'] = datetime.date.today().strftime("%Y-%m-%d")
        users[user_id]['info'] = user_info

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)

        meals = get_daily_meals()
        exercise = get_daily_exercise()
        comment = get_health_comment(weight, height, age, gender, bmr, target_weight)
        character_img = get_character_image(weight, height, age, gender, bmr)

        # D-Day 계산
        start_date = datetime.datetime.strptime(user_info['start_date'], "%Y-%m-%d").date()
        total_days = diet_period_weeks * 7
        elapsed_days = (datetime.date.today() - start_date).days
        remaining_days = total_days - elapsed_days

        if remaining_days > 0:
            d_day_text = f"D-{remaining_days}"
            alarm_message = ""
        else:
            d_day_text = "D-Day"
            if weight <= target_weight:
                alarm_message = "성공했어요! 끝까지 해내다니 정말 멋있는데요?"
            else:
                alarm_message = "아쉬워요! 다시 목표를 세워볼까요?"

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
            character_img=character_img,
            d_day_text=d_day_text,
            alarm_message=alarm_message
        )
    else:
        user_info = users.get(user_id, {}).get('info')

        # start_date는 오늘 날짜로 초기화 
        if user_info and 'start_date' not in user_info:
            user_info['start_date'] = datetime.date.today().strftime("%Y-%m-%d")
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)

        return render_template('userInfo.html', user_id=user_id, user_info=user_info)
