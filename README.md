django-admin startproject transendence ->makes transendence folder, only if there is no folder
1) docker image build -t <imagename> .
2) docker run -v $(pwd):/app -it --name <containername> <imagename>
3) change to folder with manage.py
4) python manage.py runserver ->runs server on port 8000

Adding a table to the database with django:
1) Add a new table in pong.models.py
2) After creating the new table, migrations must be made -> python manage.py makemigrations
3) After makemigration, migrate the changes -> python manage.py migrate
4) Migrations can be seen in the directory pong/migrations
 
View the database with django-admin-panel
1) create a user with admin rights -> python manage.py createsuperuser
2) go to localhost:8000/admin and log in as superuser(user: root, pw: root)
3) To see the tables in admin-panel, go to pong.admin.py and register the newly created model
