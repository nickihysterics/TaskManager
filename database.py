# database.py
import sqlite3
from datetime import datetime

class TaskManagerDB:
    def __init__(self, db_name="tasks.db"):
        # Подключение к базе данных
        self.conn = sqlite3.connect(db_name)
        # Создание таблицы, если её нет
        self.create_table()

    # Метод для создания таблицы задач в базе данных
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date DATE NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'Не выполнено'
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    # Метод для добавления задачи в базу данных
    def add_task(self, name, due_date):
        query = "INSERT INTO tasks (name, due_date) VALUES (?, ?)"
        self.conn.execute(query, (name, due_date))
        self.conn.commit()

    # Метод для получения списка задач с возможностью сортировки
    def get_tasks(self, order_by="due_date"):
        query = f"SELECT * FROM tasks ORDER BY status, {order_by}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    # Метод для обновления статуса задачи (выполнено/не выполнено)
    def update_task_status(self, task_id, status):
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        self.conn.execute(query, (status, task_id))
        self.conn.commit()

    # Метод для удаления задачи из базы данных
    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()

    # Метод для закрытия соединения с базой данных
    def close(self):
        self.conn.close()