from prometheus_client import start_http_server
from collector import OvenMediaCollector
import time
import logging

# Configure logging with timestamp, level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OvenMediaMain")

def main():
    collector = OvenMediaCollector()
    start_http_server(8000)
    logger.info("Exporter started on http://localhost:8000/metrics")
    try:
        while True:
            collector.collect()
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Exporter stopped by user")

if __name__ == "__main__":
    main()
