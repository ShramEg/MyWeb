FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir DB/details
RUN mkdir DB/removed
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
