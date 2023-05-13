from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

def create_table():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('CREATE TABLE NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')
    conn.commit()
    conn.close()

create_table()

def add_post(title, content):
    conn =sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return posts

def delete_post(post_id):
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id))
    conn.commit()
    conn.close()

def update_post(post_id, title, content):
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
    conn.commit()
    conn.close()

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        update_post(post_id, title, content)
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/')
def index()
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            add_post(title, content)
            return redirect(url_for('index'))
        return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    delete_post(post_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
