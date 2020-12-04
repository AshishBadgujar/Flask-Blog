from flask import render_template,flash,redirect,url_for,request,abort
from flask_blog.forms import RegistrationForm,LoginForm,PostForm
from flask_blog import app,bcrypt,login_manager
from flask_pymongo import ObjectId
from flask_blog.db import save_user,get_user,posts_collection,users_collection,save_post,update_post
from flask_login import login_user,logout_user,current_user,login_required
from flask_blog.models import User

login_manager.login_view='login'

@app.route('/')
@app.route('/home')
def home():
    all_posts=posts_collection.find()
    return render_template('home.html',posts=all_posts)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user=get_user(username)
        if user :  
            flash(f'user {username} already exist','danger')
        else:
            save_user(username,email,password)
            # login_user(user)
            flash(f'Account created for {username}!','success')
            return redirect(url_for('login'))
    return render_template('register.html',form=form)



@app.route('/login',methods=['GET',"POST"])
def login():
    form=LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        username=form.username.data
        password_input=form.password.data
        user=get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            flash('Your are successfully logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('incorrect username or password','danger')
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@login_manager.user_loader
def load_user(username):
    return get_user(username)



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',user=current_user)



@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        author=current_user.username
        save_post(title,content,author)
        flash('Your post has been created','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',form=form,legend='Create Post')

@app.route('/post/<id>')
def post_Detail(id):
    post=posts_collection.find_one({'_id':ObjectId(id)})
    return render_template('post_detail.html',post=post)

@app.route('/post/<id>/delete')
@login_required
def delete_post(id):
    post=posts_collection.find_one({'_id':ObjectId(id)})
    if post['author'] != current_user.username :
        abort(403)
    else:
        posts_collection.find_one_and_delete({'_id':ObjectId(id)})
    flash('Your post has been deleted','success')
    return redirect(url_for('home'))

@app.route('/post/<id>/update',methods=['GET','POST'])
@login_required
def post_update(id):
    post=posts_collection.find_one({'_id':ObjectId(id)})

    if post['author'] != current_user.username :
        abort(403)
    form=PostForm()

    if form.validate_on_submit():
        id=post['_id']
        title=form.title.data
        content=form.content.data
        update_post(id,title,content)
        flash('Your post has been updated','success')
        return redirect(url_for('post_Detail',id=post['_id']))

    elif request.method=='GET':
        form.title.data=post['title']
        form.content.data=post['content']

    return render_template('create_post.html',form=form,legend='Update Post')

