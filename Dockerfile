FROM gorialis/discord.py:master

WORKDIR /app

COPY requirements.txt ./
RUN pip install -U -r requirements.txt

CMD ["python", "-m", "chr1sbot", "--uvloop"]
