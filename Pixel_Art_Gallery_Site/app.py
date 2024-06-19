from flask import Flask, request, send_from_directory, jsonify
import sqlite3
import os

app = Flask(__name__, static_url_path='', static_folder='static')
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect('gallery.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GalleryItem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT NOT NULL,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            tools TEXT NOT NULL,
            popularity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gallery_item_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            comment TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gallery_item_id) REFERENCES GalleryItem (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    name = data['name']
    email = data['email']
    comment = data['comment']

    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Feedback (name, email, comment)
        VALUES (?, ?, ?)
    ''', (name, email, comment))
    conn.commit()
    conn.close()
    
    return jsonify(message='Форма успешно отправлена!')

@app.route('/gallery')
def gallery():
    sort_by = request.args.get('sort', 'new')
    conn = sqlite3.connect('gallery.db')
    cursor = conn.cursor()
    
    if sort_by == 'popular':
        cursor.execute('SELECT id, image, name FROM GalleryItem ORDER BY popularity DESC')
    else:  # Default to sorting by new
        cursor.execute('SELECT id, image, name FROM GalleryItem ORDER BY created_at DESC')
    
    items = cursor.fetchall()
    conn.close()
    
    gallery_items = [{'id': item[0], 'image': item[1], 'name': item[2]} for item in items]
    return jsonify(gallery_items)

@app.route('/gallery_item/<int:item_id>')
def gallery_item(item_id):
    conn = sqlite3.connect('gallery.db')
    cursor = conn.cursor()
    cursor.execute('SELECT image, name, author, tools FROM GalleryItem WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    
    cursor.execute('SELECT name, comment, date FROM Comments WHERE gallery_item_id = ? ORDER BY date DESC', (item_id,))
    comments = cursor.fetchall()
    conn.close()
    
    if item:
        return jsonify({
            'image': item[0],
            'name': item[1],
            'author': item[2],
            'tools': item[3],
            'comments': [{'name': c[0], 'comment': c[1], 'date': c[2]} for c in comments]
        })
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/submit_gallery_item', methods=['POST'])
def submit_gallery_item():
    if 'picture' not in request.files:
        return jsonify(message='No file part'), 400

    file = request.files['picture']
    if file.filename == '':
        return jsonify(message='No selected file'), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
        file.save(file_path)

        # Сохранение пути изображения без 'static' в базе данных
        image_path = file_path.replace('static/', '')

        name = request.form['name']
        author = request.form['author']
        tools = request.form['tools']

        conn = sqlite3.connect('gallery.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO GalleryItem (image, name, author, tools)
            VALUES (?, ?, ?, ?)
        ''', (image_path, name, author, tools))
        conn.commit()
        conn.close()
    
        return jsonify(message='Галерея успешно обновлена!')
    
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    gallery_item_id = data['gallery_item_id']
    name = data['name']
    comment = data['comment']

    conn = sqlite3.connect('gallery.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Comments (gallery_item_id, name, comment)
        VALUES (?, ?, ?)
    ''', (gallery_item_id, name, comment))
    conn.commit()
    conn.close()
    
    return jsonify(message='Комментарий успешно добавлен!')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    init_db()
    app.run(host='0.0.0.0', port=5000)