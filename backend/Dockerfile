FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
# upgrade to get latest security updates

RUN apt-get update        && \
    apt-get upgrade -y    && \
    apt-get autoclean -y  && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*


RUN python -m pip install --upgrade pip

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

RUN rm /app/prestart.sh /app/main.py

COPY /key.json /key.json
COPY src /app/src
COPY src/setup_scripts/start.sh /start.sh
COPY pycharm_dev_start.py /pycharm_dev_start.py
RUN chmod +x /start.sh
WORKDIR /app/src

CMD ["/start.sh"]
