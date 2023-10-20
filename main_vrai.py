import os
from googleapiclient.discovery import build
from confluent_kafka import Producer, Consumer, KafkaError
from cassandra.cluster import Cluster

# Connexion à l'API YouTube Data
API_KEY = "AIzaSyA-u35TFgqq6kNfy5-CdJ3Pzt_zQgLnq2w"

# Créez une instance de l'API YouTube Data
youtube = build("youtube", "v3", developerKey=API_KEY)
# Utilisez la méthode search.list pour obtenir les dernières vidéos
search_response = youtube.search().list(
    q="",
    type="video",
    part="id",
    maxResults=10,
    order="date"  # Triez par date pour obtenir les vidéos les plus récentes
).execute()

# Configuration du producteur Kafka
producer_config = {
    'bootstrap.servers': '172.23.0.8:9092',  # Adresse de votre cluster Kafka
}

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': '172.23.0.8:9092',  # Adresse de votre cluster Kafka
    'group.id': 'python-api',  # Groupe de consommateurs Kafka
    'auto.offset.reset': 'earliest'  # Réinitialiser l'offset pour lire depuis le début
}

# Configuration Cassandra
cassandra_host = '172.23.0.7'
cassandra_keyspace = 'python_api-keyspace'

# Créer un producteur Kafka
producer = Producer(producer_config)

# Créer un consommateur Kafka
consumer = Consumer(consumer_config)

# Parcourez les résultats et publiez les titres des vidéos dans le sujet Kafka
for search_result in search_response.get("items", []):
    if 'videoId' in search_result['id']:
        video_id = search_result['id']['videoId']
        video_info = youtube.videos().list(part="snippet", id=video_id).execute()
        if 'items' in video_info:
            video = video_info['items'][0]
            title = video['snippet']['title']
            # Publiez le titre dans le sujet Kafka
            producer.produce('python-api', key=video_id, value=title)
            print("Titre de la vidéo publié dans Kafka :", title)

# Assurez-vous de délivrer les messages au cluster Kafka
producer.flush()

# S'abonner à un topic
consumer.subscribe(['python-api'])

''' PARTIE CASSANDRA '''

# Configuration Cassandra
cluster = Cluster([cassandra_host])
session = cluster.connect(cassandra_keyspace)

# Créez un keyspace
keyspace_query = f"""
CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace}
WITH replication = {{
    'class': 'SimpleStrategy',
    'replication_factor': 3
}};
"""
session.execute(keyspace_query)

# Créez une table
table_query = f"""
CREATE TABLE IF NOT EXISTS videos (
    id uuid PRIMARY KEY,
    title text
);
"""
session.execute(table_query)

# Consommer les titres des vidéos depuis Kafka et les stocker dans Cassandra
for message in consumer:
    video_id = message.key.decode('utf-8')
    title = message.value.decode('utf-8')
    # Insérer les données dans Cassandra
    insert_query = f"INSERT INTO videos (id, title) VALUES (uuid(), %s);"
    session.execute(insert_query, (title,))

# Fermer les connexions
producer.close()
consumer.close()
session.shutdown()
cluster.shutdown()