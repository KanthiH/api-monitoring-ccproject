from kafka import KafkaProducer
import time
import logging
import random

logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers='kafka:9092')

# Different types of log messages
log_levels = {
    'info': 'API request processed successfully.',
    'warning': 'Deprecated API endpoint was used.',
    'error': 'API server returned 500 Internal Server Error.',
    'debug': 'Request payload: {"user": "test", "action": "login"}'
}

try:
    while True:
        # Randomly pick a log level
        level = random.choice(list(log_levels.keys()))
        topic = f'{level}-logs'
        message = f'{level.upper()} log: {log_levels[level]}'.encode('utf-8')

        # Send to Kafka
        producer.send(topic, value=message)
        logging.info(f"✅ Sent {level.upper()} message to Kafka topic '{topic}'")

        time.sleep(5)

except KeyboardInterrupt:
    logging.info("❌ Producer stopped by user.")
