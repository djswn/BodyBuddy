@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users:
            return "이미 존재하는 아이디입니다."

        users[user_id] = {"password": password, "info": None}
        # 회원가입 직후 사용자 정보 입력 페이지로 이동
        return redirect(url_for('userInfo', user_id=user_id))

    return render_template('register.html')
