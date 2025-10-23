@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = users.get(user_id)
        if not user or user['password'] != password:
            return "아이디 또는 비밀번호가 잘못되었습니다."

        if user['info']:  # 이미 정보가 저장된 경우
            user_info = user['info']
            bmi = calculate_bmi(user_info['weight'], user_info['height'])
            bmr = calculate_bmr(user_info['weight'], user_info['height'], user_info['age'], user_info['gender'])

            sample_meals = {
                "아침": "귀리 + 계란",
                "점심": "현미밥 + 닭가슴살",
                "저녁": "샐러드 + 연어"
            }
            sample_exercise = "30분 조깅"
            comment = "잘 하고 있어요!" if user_info['weight'] <= user_info['target_weight'] else "조심하세요, 체중이 늘고 있어요!"

            return render_template(
                'character&diet,exercise.html',
                user_info=user_info,
                bmi=bmi,
                bmr=bmr,
                meals=sample_meals,
                exercise=sample_exercise,
                comment=comment,
                weight=user_info['weight']
            )
        else:
            # 아직 사용자 정보가 없으면 userInfo로 이동
            return redirect(url_for('userInfo', user_id=user_id))

    return render_template('login.html')
