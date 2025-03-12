#! /usr/bin/env bash

# Bash format for the IDE/syntax-highlight behavior but this is more of a notes file.
# This script is not intended to be run whole by itself. Copy and use the command lines you need.


# BUILD
docker build -t stretchyagent .


# RUN
docker run -p 5000:5000 stretchyagent


# TINY TEST
curl -X POST http://localhost:5000/stress \
    -H "Content-Type: application/json" \
    -d '{"cpu_load": 50, "io_load": 0, "network_latency": 0, "database_queries": 0}'


# BASIC TEST
curl -X POST http://localhost:5000/stress \
    -H "Content-Type: application/json" \
    -d '{"cpu_load": 10, "io_load": 50, "network_latency": 2, "database_queries": 4}'


# HUGE TEST
curl -X POST http://localhost:5000/stress \
    -H "Content-Type: application/json" \
    -d '{"cpu_load": 500, "io_load": 500, "network_latency": 500, "database_queries": 500}'


# NO LOAD, NO STRESS
curl -X POST http://localhost:5000/stress \
    -H "Content-Type: application/json" \
    -d '{"cpu_load": 0, "io_load": 0, "network_latency": 0, "database_queries": 0}'




##
#

