# Read newspapers by topic Website

### Thành viên
+ **Phạm Hữu Bằng : 102190202**
+ **Lê Thị Thu Hương : 102190217**

## Requirements
Mysql Client 3.5
Python 3.7 or later

# For installing project environment

## Run following scripts in your terminal:

**Create virtual env:**
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

**Install some requirements:**
```
pip install -r requirements.txt
```

@for more information: [link](https://www.tabnine.com/blog/how-to-create-django-projects-in-pycharm-community-edition/)

# Migration
**Make migration file on changes:**
```
python manage.py makemigrations
```

**Make migration file on changes:**
```
python manage.py migrate
```

**Creating a empty migration file manually:**
```
python manage.py makemigrations <app> --empty
```

#Django

**Creating a new app (module):**
```
python manage.py startapp *module_name*
```

**Creating a superuser:**
```
python manage.py createsuperuser
```

# Dump notes

**Create new app:**
```
python manage.py startapp hello
```

**
   
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

   Collect static files (only need for `production`):
     ```
     python manage.py collectstatic --settings=core.settings.production
     ```

7. Start Server Its recommended running the `development` mode only on your local PC. If you would like to run
   the `production` mode, you should use docker / use proxy server to host static resource / or add `--insecure`
   parameter to force serving of static files with the staticfiles app (More
   detail [here](https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/)).
     ```
     cd src
     python3 manage.py runserver --settings=core.settings.development
     ```
   