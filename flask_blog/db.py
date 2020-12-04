from pymongo import MongoClient
from flask_bcrypt import generate_password_hash
from flask_blog.models import User
from flask_pymongo import ObjectId
from flask_blog import bcrypt


client=MongoClient("mongodb://localhost:27017/myDatabase")

chat_db=client.get_database('myDatabase')
users_collection=chat_db.get_collection('users')
posts_collection=chat_db.get_collection('posts')

def save_user(username,email,password):
    password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
    users_collection.insert_one({
        'username':username, 
        'email':email,
        'password':password_hash 
         })

def get_user(username):
    user_data=users_collection.find_one({'username':username})
    return User(user_data['_id'],user_data['username'],user_data['email'],user_data['password']) if user_data else None

def save_post(title,content,author):
    posts_collection.insert_one({
            'title':title,
            'content':content,
            'author':author
        })

def update_post(id,title,content):
    posts_collection.update({'_id':ObjectId(id)},
                { 
                   
                    'title':title,
                    'content':content   
                  
                })