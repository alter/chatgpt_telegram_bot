FROM python:3-alpine
WORKDIR /app
COPY requirements.txt .
ENV PATH=$PATH:/root/.local/bin
RUN /usr/local/bin/python -m pip install --user --upgrade pip
RUN pip -V
RUN pip install --user -r requirements.txt
COPY bot.py .
ENV API_KEY=""
ENV TELEGRAM_BOT_TOKEN=""
CMD ["python", "bot.py"]
