import os
# from dotenv import load_dotenv
from googleapiclient.discovery import build
from confluent_kafka import Producer

# Connexion à l'API YouTube Data
# load_dotenv()
# API_KEY = os.getenv("API_KEY")

API_KEY= "AIzaSyA-u35TFgqq6kNfy5-CdJ3Pzt_zQgLnq2w"

# Créez une instance de l'API YouTube Data
youtube = build("youtube", "v3", developerKey=API_KEY)

# Configuration du producteur Kafka
producer = Producer({'bootstrap.servers': 'localhost:9092'})


# Utilisez la méthode search.list pour obtenir les dernières vidéos
search_response = youtube.search().list(
    q="",
    type="video",
    part="id",
    maxResults=10,
    order="date"  # Triez par date pour obtenir les vidéos les plus récentes
).execute()

# Parcourez les résultats et publiez les titres des vidéos dans le sujet Kafka
for search_result in search_response.get("items", []):
    if 'videoId' in search_result['id']:
        video_id = search_result['id']['videoId']
        video_info = youtube.videos().list(part="snippet", id=video_id).execute()
        if 'items' in video_info:
            video = video_info['items'][0]
            title = video['snippet']['title']
            # Publiez le titre dans le sujet Kafka
            producer.produce('youtube-titles', key=video_id, value=title)
            print("Titre de la vidéo publié dans Kafka :", title)

# Assurez-vous de délivrer les messages au cluster Kafka
producer.flush()
