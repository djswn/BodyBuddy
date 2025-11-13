@app.route('/update_weight', methods=['POST'])
def update_weight():
    user_id = request.form['user_id']
    action = request.form['action']
    current_weight = float(request.form['weight'])

    if action == 'plus':
        current_weight += 1
    elif action == 'minus':
        current_weight -= 1
    elif action == 'set':
        current_weight = round(current_weight, 1)  # 소수점 1자리까지 반영

    users[user_id]['info']['weight'] = current_weight
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    user_info = users[user_id]['info']
    gender = user_info.get('gender', 'male')
    bmr = calculate_bmr(current_weight, user_info['height'], user_info['age'], gender)
    comment = get_health_comment(current_weight, user_info['height'], user_info['age'], gender, bmr, user_info['target_weight'])
    character_img = get_character_image(current_weight, user_info['height'], user_info['age'], gender, bmr)

    return {
        "weight": current_weight,
        "comment": comment,
        "character_img": character_img
    }
