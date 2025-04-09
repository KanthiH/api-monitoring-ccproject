from kafka import KafkaConsumer
import mysql.connector
import logging
import time

logging.basicConfig(level=logging.INFO)

# Try connecting to MySQL until it's ready
while True:
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="user",
            password="password",
            database="logdb"
        )
        break
    except:
        logging.info("⏳ Waiting for MySQL to be ready...")
        time.sleep(3)

cursor = conn.cursor()

# Create the logs table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    log_type VARCHAR(50),
    message TEXT
)
""")
conn.commit()

# Kafka consumer for all log levels
consumer = KafkaConsumer(
    'info-logs', 'warning-logs', 'error-logs', 'debug-logs',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='mysql-log-consumer'
)

logging.info("📥 Consumer started. Listening for logs...")

try:
    for msg in consumer:
        decoded = msg.value.decode('utf-8')
        log_type = decoded.split()[0].upper()  # Get "INFO", "ERROR", etc.

        # Insert into database
        cursor.execute(
            "INSERT INTO logs (log_type, message) VALUES (%s, %s)",
            (log_type, decoded)
        )
        conn.commit()
        logging.info(f"💾 Stored log → [{log_type}] {decoded}")

except KeyboardInterrupt:
    logging.info("🛑 Consumer stopped.")
finally:
    cursor.close()
    conn.close()
