# sudo docker build -t cosmos-gov-bot:0.0.1 .
# sudo docker run -it --rm --name gov-bot cosmos-gov-bot

FROM python:3-alpine

LABEL Maintainer="reecepbcups"

WORKDIR /usr/app/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./GovBot.py"]
