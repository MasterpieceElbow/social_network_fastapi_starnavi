### Starnavi's "Social network" fastapi test task

## 1.1 Installation:

Python3 should be installed

1. Install venv `python3 -m venv venv`
2. Activate venv `source venv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Launch server `uvicorn main:app --reload`
5. Check api endpoints docs:  `http://127.0.0.1:8000/docs`
6. Run tests: `python -m pytest`
7. Can authorize with `user1:password1` or `user2:password2`

## 1.2 Features:
- Login and sing up via OAuth2 and JWT
- Authentication tests
- alembic migrations
- Users, Posts, Posts' likes, Likes analytics grouped by date
- Track of users' last login and last request

## 1.3 Task requirements endpoints
- signup `POST /api/sign-up/`
- login `POST /api/token/`
- post creation `POST /api/posts/`
- like post `POST /api/posts/{post_id}/like/`
- unlike post `POST /api/posts/{post_id}/unlike/`
- likes analytics `GET /api/analytics/?date_from={date}&date_to{date}`

## 1.4 API endpoints screenshots

![](https://user-images.githubusercontent.com/80070761/207613038-3b58237f-7b2d-4109-b11e-8b287291092a.png)
![](https://user-images.githubusercontent.com/80070761/207613400-7c831d3a-c4fa-4eb4-a70a-a7fb8524c601.png)
![](https://user-images.githubusercontent.com/80070761/207613455-3556a3de-7a31-446c-9d36-09ef549e3567.png)


