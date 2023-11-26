# Импорт необходимых модулей
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QLineEdit, QCalendarWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont
from database import TaskManagerDB
from datetime import datetime

# Определение класса приложения
class TaskManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных и интерфейса
        self.db = TaskManagerDB()
        self.init_ui()

    # Инициализация интерфейса приложения
    def init_ui(self):
        # Настройки основного окна
        self.setWindowTitle('Менеджер задач')
        self.setFixedSize(600, 700)

        # Создание виджета календаря и подключение события клика
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_tasks_on_date)

        # Создание виджета списка задач и его обновление
        self.task_list = QListWidget()
        self.update_task_list()

        # Создание поля ввода и кнопок для добавления, удаления и обновления задач
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите название задачи')
        self.name_input.textChanged.connect(self.update_add_button_state)

        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(self.add_task)
        self.btn_add.setEnabled(False)

        self.btn_delete = QPushButton('Удалить')
        self.btn_delete.clicked.connect(self.delete_task)

        self.btn_done = QPushButton('Выполнено')
        self.btn_done.clicked.connect(lambda: self.update_task_status('Выполнено'))

        self.btn_undone = QPushButton('Не выполнено')
        self.btn_undone.clicked.connect(lambda: self.update_task_status('Не выполнено'))

        # Изменение шрифта для всех элементов интерфейса
        font = QFont("Times New Roman", 12)
        self.task_list.setFont(font)
        self.name_input.setFont(font)
        self.btn_add.setFont(font)
        self.btn_delete.setFont(font)
        self.btn_done.setFont(font)
        self.btn_undone.setFont(font)

        # Создание компоновки для размещения виджетов на форме
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.btn_add)

        layout.addWidget(QLabel('Название задачи и кнопка добавления'))
        layout.addLayout(input_layout)
        layout.addWidget(QLabel('Календарь'))
        layout.addWidget(self.calendar)
        layout.addWidget(QLabel('Список задач'))
        layout.addWidget(self.task_list)
        layout.addWidget(self.btn_done)
        layout.addWidget(self.btn_undone)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

        # Отображение окна
        self.show()

    # Обновление списка задач в соответствии с выбранной датой в календаре
    def show_tasks_on_date(self):
        selected_date = self.calendar.selectedDate().toPyDate()
        tasks = self.db.get_tasks(order_by="due_date")
        tasks_on_date = [task for task in tasks if task[2] == selected_date]
        self.update_task_list(tasks_on_date)

    # Обновление списка задач в виджете
    def update_task_list(self, tasks=None):
        self.task_list.clear()
        tasks = self.db.get_tasks(order_by="due_date")
        for task in tasks:
            item_text = f"{task[1]} - {task[2]} - {task[4]}"
            item = QListWidgetItem(item_text)
            item.setData(1, task[0])
            self.task_list.addItem(item)

    # Обновление состояния кнопки добавления задачи
    def update_add_button_state(self):
        self.btn_add.setEnabled(bool(self.name_input.text()))

    # Добавление новой задачи
    def add_task(self):
        name = self.name_input.text()[:15]
        due_date = self.calendar.selectedDate().toPyDate()
        self.db.add_task(name, due_date)
        self.update_task_list()
        self.name_input.clear()

    # Обновление состояния задачи (выполнено/не выполнено)
    def update_task_status(self, status):
        selected_items = self.task_list.selectedItems()
        for selected_item in selected_items:
            task_id = selected_item.data(1)
            self.db.update_task_status(task_id, status)

        self.update_task_list()
        self.task_list.clearSelection()

    # Удаление выбранных задач
    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        for selected_item in selected_items:
            task_id = selected_item.data(1)
            self.db.delete_task(task_id)

        self.update_task_list()
        self.task_list.clearSelection()

    # Обработка события закрытия окна
    def closeEvent(self, event):
        self.db.close()

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManagerApp()
    sys.exit(app.exec_())