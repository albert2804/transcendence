FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./files/ .

# here we should also set the postgresql database to be used
# its set in the settings.py file in the backend folder

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /code/backend

# Do not run this command here! we run it in the docker-compose.yml file
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# for production-server we can use for example gunicorn
# but we need to add gunicorn to requirements.txt ;)
# CMD ["gunicorn", "--bind", 0.0.0.0:8000, "backend.wsgi:application"]
