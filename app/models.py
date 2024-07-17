"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS 

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=False, default="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

    posts = db.relationship("Post", backref = "user", cascade = "all, delete")

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    tags = db.relationship('Tag', secondary='posts_tags', back_populates='posts')

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.user_id}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship('Post', secondary='posts_tags', back_populates='tags')

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"


class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"),  primary_key = True, nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key = True, nullable = False)


    def __repr__(self):
        return f"<PostTag post_id={self.post_id} tag_id={self.tag_id}>"

    
