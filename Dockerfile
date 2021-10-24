FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY secret.json .
COPY welcome.py .

CMD python welcome.py
