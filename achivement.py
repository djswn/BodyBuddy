def calculate_achievement(recommended, actual):
    if actual <= recommended:
        # 권장 이하 → 비율만큼 성취도
        ratio = (actual / recommended) * 100
    else:
        # 권장 초과 → 초과분만큼 점수 차감 ex) recommended=2000, actual=2500 → 초과 500 → 성취도 75%
        excess = actual - recommended
        penalty = (excess / recommended) * 100
        ratio = 100 - penalty

    # 범위 제한 (0~100%)
    return max(0, min(100, ratio))
