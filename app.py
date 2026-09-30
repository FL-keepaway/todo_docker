from flask import Flask, request, render_template_string, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Подключение к БД (данные берем из переменных окружения)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'todo_db')
DB_USER = os.environ.get('DB_USER', 'todo_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'StrongPass123')


def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    return conn


# Создаем таблицу при первом запуске
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


# HTML + CSS шаблон прямо в коде
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Мой Todo-лист</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f4; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; }
        ul { list-style: none; padding: 0; }
        li { border-bottom: 1px solid #eee; padding: 10px; display: flex; justify-content: space-between; }
        form { display: inline; }
        input[type=text] { padding: 8px; width: 70%; }
        button { padding: 8px 12px; background: #5cb85c; color: white; border: none; border-radius: 4px; }
        .del { background: #d9534f; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Todo List v2.0</h1>
        <form method="post" action="/add">
            <input type="text" name="task" placeholder="Введите задачу..." required>
            <button type="submit">Добавить</button>
        </form>
        <ul>
            {% for task in tasks %}
            <li>
                {{ task[1] }}
                <form method="post" action="/delete/{{ task[0] }}">
                    <button class="del" type="submit">Удалить</button>
                </form>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks ORDER BY id ASC;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (title) VALUES (%s)', (task,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
