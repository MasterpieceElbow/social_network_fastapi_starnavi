### Starnavi's "Social network" async fastapi test task

## 1.1 Installation:

Python3 should be installed

Venv:
- Install venv `python3 -m venv venv`
- Activate venv `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
   
DB:
- Metadata: user:`postgres`, password:`postgres`, host:`localhost`, dbname: `social_network`
- Make migrations `alembic upgrade head`
- Restore data `psql social_network < db.dump`

Run server:
- Launch server `uvicorn main:app --reload`
- Check api endpoints docs:  `http://127.0.0.1:8000/docs`
   
Tests:
- Run tests: `python -m pytest`
  
Authorize
- Can authorize with `user1:pass1` or `user2:pass1`

## 1.2 Features:
- Asynchronous views and PostgreSQL queries
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
- likes analytics `GET /api/analytics/?date_from={date}&date_to={date}`
- user activity (last_login, last_request) `GET /api/users/{user_id}/`

**Note**: all endpoints, except `login` and `signup` are allowed only for authenticated user.

## 1.4 API endpoints screenshots

![](https://user-images.githubusercontent.com/80070761/207613038-3b58237f-7b2d-4109-b11e-8b287291092a.png)
![](https://user-images.githubusercontent.com/80070761/207613400-7c831d3a-c4fa-4eb4-a70a-a7fb8524c601.png)
![](https://user-images.githubusercontent.com/80070761/207613455-3556a3de-7a31-446c-9d36-09ef549e3567.png)


