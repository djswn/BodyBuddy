# BodyBuddy
현대인의 체중 관리와 건강한 습관 형성을 돕기 위해 개발되었습니다. 사용자의 정보를 입력받아 BMI/BMR, 권장 칼로리 계산과 맞춤형 식단 구성등을 제공합니다.
## 멤버구성
 - 강지민(JM030220)
 - 차언주(djswn)
 - 최지웅(cjww543210)
## 데모 화면
<img width="1440" height="900" alt="main" src="https://github.com/user-attachments/assets/868107bd-93d6-41d5-9bf5-b58e846297ce" />
## 프로젝트 구조
```
BodyBuddy/
├── utils/      # 계산 함수
├── static/     # CSS ,JS, 이미지 파일 
├── templates/  # HTML 템플릿
├── app.py      # Flask 메인 실행 파일
├── README.md
└── CONTRIBUTING.md
```
## 기술 스택
- Python
- Flask
- Bootstrap
- HTML5 / CSS3
- JavaScript (Ajax)
- JSON 데이터 처리
## 개발 환경
```
pip install flask
```
## 실행 방법
```
git clone https://github.com/djswn/BodyBuddy.git
cd bodyBuddy
python app.py
```
http://127.0.0.1:5000 접속
## 주요 기능
1. 회원가입, 로그인 기능
2. 사용자 정보 기록
3. 개인의 BMI, BMR, 권장칼로리 계산
4. 상황에 따른 자동 멘트
5. 추천 식단 드롭다운 제시
6. 체중에 따라 동적 변화하는 캐릭터 화면
7. 체중 정보를 저장하여 나타내는 변동 그래프
8. 설정한 목표 기간이 다 되었을 때, 목표 체중 사이의 알림 기능
## 향후 개선 계획
- 다국어 지원
- 모바일 최적화
- 사용자를 위한 여러 알림 기능
## CONTACT
cej0836@naver.com
