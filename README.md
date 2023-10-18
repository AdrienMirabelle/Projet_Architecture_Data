# Projet_Architecture_Data

# Lancer le script du docker compose.yml
docker-compose up

# Lancer dans un autre terminal pour accéder au cqls de cassandra
docker run -it --network=projet_architecture_data_cassandra-net --rm cassandra cqlsh cassandra