# Utilisez l'image Python comme base
FROM python:3.8-slim

# Copiez votre script Python dans le conteneur
COPY main_vrai.py ./main_vrai.py

# Installez les dépendances requises (par exemple, confluent-kafka)
RUN pip install confluent-kafka google-api-python-client cassandra-driver

# Spécifiez le script à exécuter lorsque le conteneur démarre
CMD ["python", "./main_vrai.py"]