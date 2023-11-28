FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./files/ .
# COPY ./files/ /code/

RUN pip install -r requirements.txt

EXPOSE 8000

# CMD ["tail", "-f", "/dev/null"]
WORKDIR /code/backend
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# for production-server we can use for example gunicorn
# but we need to add gunicorn to requirements.txt ;)
# CMD ["gunicorn", "--bind", 0.0.0.0:8000, "backend.wsgi:application"]
