from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # 첫 화면: 사용자 입력 폼
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # 폼에서 전달된 값 가져오기
    user_info = {
        "name": request.form['name'],
        "age": int(request.form['age']),
        "height": float(request.form['height']),
        "weight": float(request.form['weight']),
        "body_fat": float(request.form['body_fat']),
        "target_weight": float(request.form['target_weight']),
        "diet_period_weeks": int(request.form['diet_period_weeks'])
    }
    # 결과 페이지로 값 전달
    return render_template('result.html', user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True)
