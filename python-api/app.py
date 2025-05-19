from flask import Flask
from dotenv import load_dotenv
import mysql.connector 
from app.controllers.message_controller import MessageController


import os

load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello():
    db = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = db.cursor()
    cursor.execute("SELECT 'Hello from Flask and MySQL!'")
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0]



@app.route('/messages', methods=['POST'])
def store_message():
    return message_controller.store_message()

@app.route('/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    return message_controller.get_messages(user_id)

message_controller = MessageController()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)








