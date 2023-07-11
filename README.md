# jwt-auth

## 프로젝트 설정

회원가입 기능이 아직 구현되지 않았으므로 로그인 기능 테스트를 위해선 유효한 사용자 정보를 직접 DB에 포함하도록 한다.

### macOS/Linux
```bash
git clone https://github.com/Lion-11th-Team/jwt-oauth.git
cd jwt-oauth
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements
python3 manage.py migrate
```

### Windows
###
```bash
git clone https://github.com/Lion-11th-Team/jwt-oauth.git
cd jwt-oauth
python -m venv venv
source venv/Scripts/activate
pip install -r requirements
python manage.py migrate
```
