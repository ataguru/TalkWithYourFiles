# Dockerfile
FROM python:3.9.16

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./TalkWithYourFiles /app

EXPOSE 8501

CMD streamlit run /app/streamlit_interface.py --server.address 0.0.0.0