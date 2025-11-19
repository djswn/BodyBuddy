def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = users.get(user_id)
        if not user or user['password'] != password:
            # 로그인 실패
            return render_template('login.html', error="아이디 또는 비밀번호가 잘못되었습니다.")
==============================================================================================
return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
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
