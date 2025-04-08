# producer.py
from kafka import KafkaProducer
import time
import logging

logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers='kafka:9092')

try:
    while True:
        message = b"API log: something happened"
        producer.send('info-logs', value=message)
        logging.info("✅ Message sent to Kafka topic 'info-logs'")
        time.sleep(5)  # Wait 5 seconds between messages
except KeyboardInterrupt:
    logging.info("❌ Producer stopped by user.")
