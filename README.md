# meta-local
Run and develop Meta app in your local computer

![Meta platform](https://rwstatic.ru/h/meta/avatar.png)

## What is it?
- This stub run Meta with Test PostgreSQL database into your local computer.

## Develop
- Change code in src dir
- Run `pip3 install -r requirements.txt`
- Run Python3 `python build.py` or `python3 build.py`
- Run `docker-compose restart`
- Run `yoyo apply --database postgresql://todo_usr:todo_pass@localhost/todo_db ./migrations`
- Open http://localhost:8089/