#! /usr/bin/env python

import requests
import time
import random
import logging


target_url = 'http://hostname.com:5000/stress'


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_load(url, cpu_load, io_load, network_latency, database_queries, request_rate):
    while True:
        payload = {
            'cpu_load': cpu_load,
            'io_load': io_load,
            'network_latency': network_latency,
            'database_queries': database_queries
        }

        try:
            start_time = time.time()
            response = requests.post(url, json=payload)
            end_time = time.time()

            # Log response time
            response_time = end_time - start_time
            logger.info(f"Load generated: CPU Load {cpu_load}, IO Load {io_load}, "
                        f"Network Latency {network_latency}, DB Queries {database_queries}, "
                        f"Response Time: {response_time:.2f} seconds")

            # Check for success
            if response.status_code == 200:
                logger.info(f"Request Success: {response.json()}")
            else:
                logger.error(f"Request Failed: {response.status_code}, {response.text}")

        except Exception as e:
            logger.error(f"Error during request: {e}")

        # Simulate request rate by sleeping
        time.sleep(1 / request_rate)  # Adjust request rate per second


if __name__ == "__main__":
    target_url = "https://api.runpod.ai/v2/norx0cd12ei4ap/run"

    # Randomize load levels for variety in testing
    cpu_load = random.randint(1, 100)
    io_load = random.randint(1, 100)
    network_latency = random.randint(0, 500)  # Random latency in ms
    database_queries = random.randint(0, 100)  # Random number of database queries
    request_rate = 10  # Number of requests per second

    generate_load(target_url, cpu_load, io_load, network_latency, database_queries, request_rate)


##
#

