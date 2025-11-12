def get_character_image(weight, height, age, gender, bmr):
    bmi = calculate_bmi(weight, height)

    if gender == 'male':
        if bmi < 18.5:
            # 저체중 남성 → 마른 가나디
            return url_for('static', filename='images/thin_ganadi.png')
        elif 18.5 <= bmi < 23:
            # 정상 남성 → 일반 가나디
            return url_for('static', filename='images/ganadi.png')
        else:
            # 과체중/비만 남성 → 뚱뚱한 가나디
            return url_for('static', filename='images/fat_ganadi.png')

    elif gender == 'female':
        if bmi < 18.5:
            # 저체중 여성 → 마른 고냐니
            return url_for('static', filename='images/thin_gonyani.png')
        elif 18.5 <= bmi < 23:
            # 정상 여성 → 일반 고냐니
            return url_for('static', filename='images/gonyani.jpeg')
        else:
            # 과체중/비만 여성 → 뚱뚱한 고냐니
            return url_for('static', filename='images/fat_gonyani.png')
