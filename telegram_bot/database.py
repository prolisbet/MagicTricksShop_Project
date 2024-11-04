import sqlite3
import django
from django.contrib.auth.hashers import check_password
import sys
import os

# Добавьте путь к проекту Django в sys.path
sys.path.append('../django_project/MagicTricksShop')

# Установите значение DJANGO_SETTINGS_MODULE в переменную окружения
django_project_name = 'MagicTricksShop'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{django_project_name}.settings')

# Инициализируйте Django
django.setup()

DB_PATH = '../django_project/MagicTricksShop/db.sqlite3'


def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopUsers_user WHERE name=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_admin_by_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Получаем пароль из базы данных
    cursor.execute("SELECT * FROM auth_user WHERE username=?", (username,))
    admin = cursor.fetchone()
    conn.close()

    if admin:
        # Предполагая, что хеш пароля находится в столбце с индексом 1 (замените на нужный индекс)
        hashed_password = admin[1]
        if check_password(password, hashed_password):
            return admin
    return None

    # conn = sqlite3.connect(DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM auth_user WHERE username=? AND password=?", (username, password))
    # admin = cursor.fetchone()
    # conn.close()
    # return admin


def get_orders_by_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopOrders_order WHERE user_id=?", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders


def get_order_details(order_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT shopOrders_orderitem.quantity, shopGoods_product.name, shopGoods_product.price
        FROM shopOrders_orderitem
        JOIN shopGoods_product ON shopOrders_orderitem.product_id = shopGoods_product.id
        WHERE shopOrders_orderitem.order_id=?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items


def get_all_orders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shopOrders_order")
    orders = cursor.fetchall()
    conn.close()
    return orders


def get_analytics_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Получаем общее количество завершенных заказов
    cursor.execute("SELECT COUNT(*) FROM shopOrders_order WHERE status='completed'")
    total_sales = cursor.fetchone()[0]

    # Получаем общую прибыль от завершенных заказов
    cursor.execute("""
        SELECT SUM(shopOrders_orderitem.quantity * shopGoods_product.price)
        FROM shopOrders_orderitem
        JOIN shopOrders_order ON shopOrders_orderitem.order_id = shopOrders_order.id
        JOIN shopGoods_product ON shopOrders_orderitem.product_id = shopGoods_product.id
        WHERE shopOrders_order.status='completed'
    """)
    total_profit = cursor.fetchone()[0] or 0

    conn.close()
    return total_sales, total_profit


def get_reports_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, sales_data, profit, expenses FROM shopOrders_report ORDER BY date DESC")
    reports = cursor.fetchall()
    conn.close()
    return reports
