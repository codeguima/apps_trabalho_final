from app.config import Config
import mysql.connector

class Message:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        self.cursor = self.db.cursor(dictionary=True)

    def save(self):
        query = """
        INSERT INTO messages (sender_id, receiver_id, content, status)
        VALUES (%s, %s, %s, 'pending')
        """
        values = (self.sender_id, self.receiver_id, self.content)
        self.cursor.execute(query, values)
        self.db.commit()
        self.id = self.cursor.lastrowid
        return self.id

    @classmethod
    def get_by_user(cls, user_id):
        instance = cls()
        query = """
        SELECT * FROM messages 
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY created_at DESC
        """
        instance.cursor.execute(query, (user_id, user_id))
        return instance.cursor.fetchall()

    @classmethod
    def get_by_id(cls, message_id):
        instance = cls()
        query = "SELECT * FROM messages WHERE id = %s"
        instance.cursor.execute(query, (message_id,))
        return instance.cursor.fetchone()

    @classmethod
    def update_status(cls, message_id, status):
        instance = cls()
        query = "UPDATE messages SET status = %s WHERE id = %s"
        instance.cursor.execute(query, (status, message_id))
        instance.db.commit()
        return instance.cursor.rowcount > 0