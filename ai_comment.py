def ai_comment(achievement):
    if achivement < 10:
        return "분발하세요! 이대로는 안돼요!"
    elif achivement < 30:
        return "오늘처럼은 안된다는거 알고 계시죠?"
    elif achievement < 50:
        return "오늘은 무난했어요. 내일도 잘 조절해보죠!"
    elif achivement < 70:
        return "점점 나아지고 있는 당신, 멋있는데요?"
    elif achievement < 90:
        return "좋아요! 지금처럼만 하면 목표에 가까워질 거예요."
    else:
        return "완벽합니다! 앞으로도 꾸준히 유지해보세요."
