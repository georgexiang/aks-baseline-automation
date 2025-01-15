import logging
import os

import psycopg2
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

# 设置日志
logging.basicConfig(level=logging.DEBUG)

# PostgreSQL 数据库连接
def get_db_connection():
    conn = psycopg2.connect(
        host='flask-test.postgres.database.azure.com',
        port=5432,
        user='admin123',
        password='Welcome1',  # 请替换为实际的数据库密码
        database='flask-test',
        sslmode='require'  # Azure PostgreSQL 需要 SSL 连接
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/players')
def players():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM players;")
        players_data = cur.fetchall()  # 获取所有玩家数据
        cur.close()
        conn.close()

        # 将数据传递到模板
        return render_template('players.html', players=players_data)

    except Exception as e:
        app.logger.error(f"Error querying the players table: {e}")
        return f"Error: {e}"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
