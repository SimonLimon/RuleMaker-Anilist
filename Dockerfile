FROM python
WORKDIR /app
COPY . /app

# Set environment variables
ENV anilistuserid="-1"
ENV client_id="-99999"
ENV client_secret="secret"
ENV torrentHost="localhost"
ENV torrentPort="8181"
ENV torrentUsername="admin"
ENV torrentPassword="admin"
ENV feeds=","
ENV rootSavePath="/media/anime/"
ENV sleepTime="1440"


RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-u", "main.py"]