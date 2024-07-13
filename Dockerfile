FROM python:3.9

WORKDIR /ReactBot

ADD ./cogs ./cogs
ADD ./config.py .
ADD ./main.py .


RUN pip install discord.py==1.7.3

CMD ["python", "-u", "./main.py"]