
from flask import Flask, request, jsonify
import time
import os
import multiprocessing
import threading
import random
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to stress CPU
def stress_cpu(cpu_load: int):
    """Simulate CPU load by running a busy loop"""
    count = 0
    while count < cpu_load * 1000:
        count += 1


# Function to stress I/O
def stress_io(io_load: int):
    """Simulate I/O load by reading and writing files"""
    for _ in range(io_load):
        with open("/tmp/stress_test_file.txt", "w") as f:
            f.write("A" * 10 ** 6)  # Writing 1MB to the file
        with open("/tmp/stress_test_file.txt", "r") as f:
            f.read()  # Reading the file


# Function to simulate network latency
def stress_network_latency(latency: int):
    """Simulate network latency by sleeping"""
    time.sleep(latency / 1000.0)  # Latency is in milliseconds, convert to seconds


# Function to simulate database load (just a delay for now)
def stress_database_load(query_count: int):
    """Simulate database load by introducing delays"""
    for _ in range(query_count):
        time.sleep(0.1)  # Simulate a 100ms delay for each database query


# API endpoint to control stress levels
@app.route('/stress', methods=['POST'])
def stress():
    data = request.json
    cpu_load = data.get('cpu_load', 0)  # 0 to 100 range
    io_load = data.get('io_load', 0)  # 0 to 100 range
    network_latency = data.get('network_latency', 0)  # 0 to 500 ms range
    database_queries = data.get('database_queries', 0)  # 0 to 100 queries

    cpu_processes = []
    io_threads = []
    network_threads = []
    db_threads = []

    # Simulate CPU load in parallel processes
    for _ in range(cpu_load):
        process = multiprocessing.Process(target=stress_cpu, args=(cpu_load,))
        process.start()
        cpu_processes.append(process)

    # Simulate IO load in parallel threads
    for _ in range(io_load):
        thread = threading.Thread(target=stress_io, args=(io_load,))
        thread.start()
        io_threads.append(thread)

    # Simulate network latency in parallel threads
    for _ in range(network_latency):
        thread = threading.Thread(target=stress_network_latency, args=(random.randint(0, network_latency),))
        thread.start()
        network_threads.append(thread)

    # Simulate database load in parallel threads
    for _ in range(database_queries):
        thread = threading.Thread(target=stress_database_load, args=(random.randint(0, database_queries),))
        thread.start()
        db_threads.append(thread)

    # Wait for threads and processes to complete
    for process in cpu_processes:
        process.join()

    for thread in io_threads + network_threads + db_threads:
        thread.join()

    # Log the activity and return the response
    logger.info(
        f"CPU Load: {cpu_load}, IO Load: {io_load}, Network Latency: {network_latency}, Database Queries: {database_queries}")

    return jsonify({"status": "success", "cpu_load": cpu_load, "io_load": io_load,
                    "network_latency": network_latency, "database_queries": database_queries})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


##
#

