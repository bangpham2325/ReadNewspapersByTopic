# 19N12 - TEAM 5 - Charity: Corporate Social Responsibility Hub

### Thành viên
+ **Phạm Hữu Bằng : 102190202**
+ **Lê Thị Kim Chi :102190204**
+ **Nguyễn Vũ Phúc Nguyên : 10219028**
+ **Lê Thị Thu Hương : 102190217**
+ **Dương Anh Tuấn : 102190296**
+ **Lâm Toàn : 102190193**
+ **Nguyễn Luật : 102190274**

## Volunteer Website

### Overview

***Việt Nam hay thế giới của chúng ta đang có rất nhiều những gia đình, những tập thể, những cá nhân có hoàn cảnh éo le, áp lực trong cuộc sống. Bên cạnh đó có những nhà hảo tâm, những tổ chức phi chính phủ, những tình nguyện viên trẻ mong muốn chung tay góp sức giúp đỡ những trường hợp gặp khó khăn. Và VOLUNTEER là nền tảng ra đời để làm nơi tụ hội cho những tổ chức, những tình nguyện viên ấy có thêm nhiều cơ hội cùng chung tay góp sức giúp đỡ cho những trường hợp gặp khó khăn như vậy một cách nhanh chóng.***

### Feature

- **Cá nhân hay những tổ chức có thể tự tạo ra những chiến dịch từ thiện để kêu gọi sự giúp đỡ của mọi người, những tình nguyện viên, tổ chức khác tham gia vào chiến dịch của mình.**
- **Với chiến dịch của mình người tạo có thể thêm những bài đăng trạng thái để chia sẻ tiến độ, cập nhật tình hình của dự án bao gồm ngân sách, thành viên tham gia..., những tình nguyên viên tham gia đăng ký tham gia có thể thảo luận chung, góp ý ở các bài đăng tiến độ hay ngay trong group trò chuyện (đoạn chat chung của tất cả thành viên trong chiến dịch).**
- **Ngoài ra với mỗi chiến dịch, tình nguyện viên còn có thể nêu lên những cảm nhận thông qua việc viết nhận xét cho dự án, làm tăng tính minh bạch cho chiến dịch**


### Link
* #### link video demo: https://drive.google.com/file/d/1gctAb6O3hTxiXFrQLbDgauOoOlb_vLpr/view?usp=sharing
* #### link slide: https://www.canva.com/design/DAFS1TiHc1I/LiFGiiQ4mKSIk8VpHAv-ow/edit?utm_content=DAFS1TiHc1I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
* #### link web : http://146.190.92.238/
## Requirements
Mysql Client 3.5,
Python 3.8 or later,
Vue 3.2.13 or later

## Install dependencies and build

### Running in ubuntu

1. Install packages

     ```
     sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev npm vue@next @vue/cli
     ```

2. Create virtualenv
     ```
     WIN
     python -m venv env
     env\Scripts\activate
     virtualenv --python=/usr/bin/python3 env
     source /home/ubuntu/env/bin/activate
     deactivate
     ```

3. Install all dependencies:
     ```
     pip3 install -r requirements.txt
     ```

4. Init config & database
     ```
     ./ci/generate-rsa-key.sh jwt
     cp src/core/config.env.sample src/config.env
     cd src
     python3 manage.py migrate
     ```

5. Get Google Calendar API credentials
     ```
     https://developers.google.com/calendar/quickstart/go
     ```

6. Build frontend

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

### Running in windows

1. Install environment and activate :
    ```
     python -m venv venv
     venv\Scripts\activate
    ```

2. Install requirement libraries :

- First you have to comment libraries uWSGI (this only run in Ubuntu)
    ```
     pip install -r requirements.txt
    ```

3. Follow from step 3 to the end in Running with Ubuntu

## Using docker

If you would like to use docker, you can skip the `Install dependencies and build` section. Just follow these steps:

1. Copy and rename these files. Then change the values for `__ERP_PORT__`, `__DJANGO_SETTINGS_MODULE__`, and other environment variables (if needed).
    * `ci/Dockerfile.template` -> `Dockerfile`
    * `ci/docker-compose.yml.local` -> `docker-compose.yml`
    * `ci/docker.env.template` -> `docker.env`
    * `src/core/config.env.sample` -> `src/config.env`
2. From the root folder (where the docker-compose.yml located), run the command:
     ```
     docker-compose up -d --build
     ```

## Adding libraries

1. Adding python libraries:

   If your need add more libraries while developing new feature. Make sure to follow these steps:

   a. First, install the library:
     ```
     pip install <library name>
     ```

   b. Use the library as you want

   c. List the libraries to the requirements.txt
     ```
     pip freeze > requirements.txt
     ```

   d. Commit the requirements.txt within your other codes

2. Adding JavaScript libraries:
   If your need add more JavaScript libraries for frontend. Make sure to follow these steps:

   a. First, install the library (from `src/frontend` folder):
    ```
    npm install <library name>
    ```

    b. Use the library as you want

    d. Commit these files within other changes to gitlab:
    * src/frontend/package.json
    * src/frontend/package-lock.json

