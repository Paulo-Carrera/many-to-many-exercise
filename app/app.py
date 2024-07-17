"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "P@ulo445"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def list_users():
    users = User.query.all()
    tags = Tag.query.all()
    return render_template('users.html', users = users, tags = tags)


@app.route('/users/new', methods = ['GET'])
def new_user():
    return render_template('new_user.html')


@app.route('/users/new', methods = ['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None 

    new_user = User(first_name = first_name , last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all()
    return render_template('user_detail.html', user = user, posts = posts)


@app.route('/users/<int:user_id>/edit', methods = ['GET'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags = tags)


@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title = title, content = content, user = user)

    tag_ids = request.form.getlist('tags')
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post.tags.extend(tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user', user_id = user_id))


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)  # Fetch the user associated with the post
    tags = post.tags    # Access the tags associated with the post
    return render_template('post_detail.html', post = post, tags = tags, user = user)


@app.route('/posts/<int:post_id>/edit', methods = ['GET'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = request.form.getlist('tags')
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags  # Update the post's tags

    db.session.commit()

    return redirect(url_for('show_post', post_id = post_id))


@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user', user_id = post.user_id))


@app.route('/add-tag', methods = ['GET'])
def new_tag():
    return render_template('add_tag.html')

@app.route('/add-tag', methods = ['POST'])
def create_tag():
    name = request.form['name']
    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)



@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.filter(Post.tags.contains(tag)).all()
    return render_template('tag_detail.html', tag=tag, posts = posts)



# @app.route('/edit-tag/<int:tag_id>', methods = ['GET'])
# def edit_tag(tag_id):


if __name__ == '__main__':
    app.run(debug=True)



