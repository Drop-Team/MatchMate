FROM python:3.10

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /bot/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY . /bot

CMD ["python", "bot.py"]