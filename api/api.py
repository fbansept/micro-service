from flask import Flask, jsonify
import redis
import os
from datetime import datetime
import logging

app = Flask(__name__)
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

logging.basicConfig(filename='/var/log/flask/api.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/givetime', methods=['GET'])
def give_time():
    container_name = os.uname()[1]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    redis_client.lpush('times', f'{container_name}: {current_time}')
    logger.info(f'Time requested from container: {container_name}')
    return jsonify({'container': container_name, 'time': current_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)