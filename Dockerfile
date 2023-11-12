FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY ./app /app/app

RUN pip install --no-cache-dir -r /app/app/requirements.txt

ENV DATABASE_URL mysql+mysqlconnector://root:secret@db:3306/ecommerce-store

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
