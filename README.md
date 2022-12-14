### Starnavi's "Social network" fastapi test task

## 1.1 Installation:

Python3 should be installed

1. Install venv `python3 -m venv venv`
2. Activate venv `source venv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Launch server `uvicorn main:app --reload`
5. Check api endpoints docs:  `http://127.0.0.1:8000/docs`
6. Run tests: `python -m pytest`

## 1.2 Features:
- Login and sing up via OAuth2 and JWT
- Authentication tests
- alembic migrations
- Users, Posts, Posts' likes, Likes analytics grouped by date