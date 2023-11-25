FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./conf/requirements.txt .

RUN pip install -r requirements.txt

COPY ./files .

EXPOSE 8000

CMD ["tail", "-f", "/dev/null"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
