FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY components /app/components
COPY data /app/data
COPY main.py /app/main.py

ENTRYPOINT ["streamlit", "run", "main.py"]
