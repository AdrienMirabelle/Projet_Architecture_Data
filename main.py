from confluent_kafka import Producer, Consumer, KafkaError

# Configuration du producteur Kafka
producer_config = {
    'bootstrap.servers': '172.23.0.8:9092',  # Adresse de votre cluster Kafka
}

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': '172.23.0.8:9092',  # Adresse de votre cluster Kafka
    'group.id': 'my-consumer-group',  # Groupe de consommateurs Kafka
    'auto.offset.reset': 'earliest'  # Réinitialiser l'offset pour lire depuis le début
}

# Créer un producteur Kafka
producer = Producer(producer_config)

# Créer un consommateur Kafka
consumer = Consumer(consumer_config)

# Publier un message sur un topic
producer.produce('mon-topic', key='cle', value='valeur')

# Attendre que le message soit envoyé
producer.flush()

# S'abonner à un topic
consumer.subscribe(['mon-topic'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Fin de la partition atteinte, consommation terminée.')
        else:
            print('Erreur de consommation: {}'.format(msg.error()))
    else:
        print('Reçu un message: key={}, value={}'.format(msg.key(), msg.value()))

# Fermer le consommateur
consumer.close()
