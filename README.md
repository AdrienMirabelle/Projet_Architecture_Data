# Projet_Architecture_Data

# Lancer le script du docker compose.yml
docker-compose up -d

# Arrêté le script docker compose qui tourne en arrière plan
docker-compose down

# Lancer dans un autre terminal pour accéder au cqls de cassandra
docker run -it --network=projet_architecture_data_cassandra-net --rm cassandra cqlsh cassandra

# Rentrer dans un container docker
docker exec -it "nom container" /bin/bash

# Lister les topics de kafka
kafka-topics.sh --list --bootstrap-server kafka-node:9092

# Lister les consumers de kafka
kafka-consumer-groups.sh --list --bootstrap-server kafka-node:9092

# Récupérer l'addresse
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-node
