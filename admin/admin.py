from flask import Flask, render_template_string
import redis
import os
import logging

app = Flask(__name__)
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

logging.basicConfig(filename='/var/log/flask/admin.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/admin', methods=['GET'])
def admin():
    times = redis_client.lrange('times', 0, -1)
    times = [time.decode('utf-8') for time in times]
    html = '<ul>' + ''.join(f'<li>{time}</li>' for time in times) + '</ul>'
    logger.info('Admin page accessed')
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)