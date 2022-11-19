FROM python:3.7
ENV token token_init
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["python3.7", "./bot_starting.py"]