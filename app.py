from os import name
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlockPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Block post : " + str(self.id)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/posts", methods=['POST', 'GET'])
def post():
    print("method  called")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = BlockPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = BlockPost.query.all()

        return render_template("post.html", posts=all_post, len=len(all_post))


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlockPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        post = BlockPost.query.get_or_404(id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        post = BlockPost.query.get_or_404(id)
        title = post.title
        content = post.content
        return render_template('edit.html', title=title, content=content, id=id)


if __name__ == "__main__":
    app.run(debug=True)
