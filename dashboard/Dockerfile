FROM python:3.8

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["greppo", "serve", "app.py", "0.0.0.0", "8082"]

EXPOSE 8082