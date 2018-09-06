from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:geveland12@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '123456789'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self,title,body):
        self.title = title
        self.body = body 

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():
    if request.args.get('id'):
        blog_posts = Blog.query.filter_by(id=request.args.get('id')).all()
        body = blog_posts[0].body
    else:
        blog_posts = Blog.query.filter_by().all()
        body = ''
    return render_template('blog.html', blog_posts=blog_posts)


@app.route('/newpost', methods=['POST', 'GET'])
def new_blog_post():
    if request.method =="POST":
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('newpost.html')



if __name__ == '__main__':
    app.run()