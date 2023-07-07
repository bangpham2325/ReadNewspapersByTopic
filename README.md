# Read newspapers by topic Website

### Thành viên
+ **Phạm Hữu Bằng : 102190202**
+ **Lê Thị Thu Hương : 102190217**

## Requirements
Mysql Client 2.1
Python 3.8 or later
Mysql Server 8.0

# For installing project environment

## Run following scripts in your terminal:

**Create virtual env in windows:**
```
python -m venv env
```

**Activate virtual env:**
```
env\Scripts\activate
```

*(option) If you want to deactivate:*
```
env\Scripts\deactivate
```

**Create virtual env in ubuntu:**
```
python3.8 -m venv env
```

**Activate virtual env:**
```
source env/bin/activate
```

*(option) If you want to deactivate:*
```
deactivate
```

**Install some requirements:**
```
pip install -r requirements.txt
```

@for more information: [link](https://www.tabnine.com/blog/how-to-create-django-projects-in-pycharm-community-edition/)

**Create file .env the same .envexample**

**Install some requirements:**
```
pip install -r requirements.txt
```

# Migration
**Make migration file on changes:**
```
python manage.py makemigrations
```

**Make migration file on changes:**
```
python manage.py migrate
```

**Run server backend:**
```
python manage.py runserver
```


**Run backend using docker:**
```
docker pull bangpham2325/backend-image:latest
docker-compose up -d
```


**Creating a superuser:**
```
python manage.py createsuperuser
```

**Collect static files (only need for `production`):** 
```
python manage.py collectstatic --settings=core.settings
```

# Run Front-end
   
### Build frontend

   Copy *src/frontend/sample.env* to *src/frontend/.env*, and change the config if you want. By default, we don't need
   to change.

   Build the frontend (call these command from the *src/frontend* folder):

   Install dependencies
     ```
     npm install
     ```

   Build for release
     ```
     npm run build
     ```

   Or build for debug
     ```
     npm run watch
     ```



