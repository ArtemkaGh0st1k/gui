import sqlite3
from os.path import exists
from os import remove


class Dbhelper:

    @staticmethod
    def create_test_db(db_name="lab3/test_db_lab3.db"):
        if exists(db_name):
            remove(db_name)
        print(f"Старый файл {db_name} удален.")

        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # таблица пользователей 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT DEFAULT 'user'
                )
            ''')

            users_data = [
                ('Иван Иванов', 'ivan@example.com', 'admin'),
                ('Анна Смирнова', 'anna@example.com', 'user'),
                ('Петр Петров', 'petr@example.com', 'user'),
                ('Елена Сидорова', 'elena@example.com', 'manager')
            ]
            cursor.executemany('INSERT INTO users (name, email, role) VALUES (?, ?, ?)', users_data)

            # таблица товаров 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER DEFAULT 0
                )
            ''')

            products_data = [
                ('Ноутбук', 75000.00, 10),
                ('Смартфон', 45000.50, 25),
                ('Беспроводные наушники', 8900.00, 50),
                ('Клавиатура', 3500.00, 15)
            ]
            cursor.executemany('INSERT INTO products (title, price, stock) VALUES (?, ?, ?)', products_data)

            # таблица заказов (orders)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')

            orders_data = [
                (1, 1, 1),
                (2, 2, 2),
                (3, 3, 1),
                (2, 4, 1)
            ]
            cursor.executemany('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)', orders_data)

            # сохраняем изменения
            conn.commit()

            print(f"База данных '{db_name}' успешно создана и заполнена тестовыми данными!")