# import the flask web framework
import json
import redis as redis
from flask import Flask, request
from loguru import logger

HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

# create a Flask server, and allow us to interact with it using the app variable
app = Flask(__name__)


def get_current_engine_temperature(database):
    # Get the most recent engine temperature from the database
    engine_temperature_values = database.lrange(DATA_KEY, 0, 0)
    if not engine_temperature_values:
        return None
    return float(engine_temperature_values[0])


def get_average_engine_temperature(database):
    # Get all engine temperature values from the database
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    if not engine_temperature_values:
        return None
    # Calculate the average engine temperature
    average_temperature = sum(float(temp) for temp in engine_temperature_values) / len(engine_temperature_values)
    return average_temperature


# define an endpoint which accepts POST requests, and is reachable from the /record endpoint
@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200


# practically identical to the above
@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    current_engine_temperature = get_current_engine_temperature(database)
    average_engine_temperature = get_average_engine_temperature(database)
    return {
        "current_engine_temperature": current_engine_temperature,
        "average_engine_temperature": average_engine_temperature,
        "success": True
    }, 200
