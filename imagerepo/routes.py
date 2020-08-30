from flask import render_template, request, flash, url_for, redirect
from imagerepo import app, db
from imagerepo.forms import Register, Login, Upload, SearchUser
from imagerepo.models import User, Image
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from PIL import Image as pilImage
import imagehash
import os


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchUser()
    if form.validate_on_submit():
        return redirect(url_for('user', username=form.username.data))

    images = None
    # load all the images upload by the logged in user
    if current_user.is_authenticated:
        images = current_user.images
    return render_template('home.html', title="Home", form=form, images=images)


@app.route("/user/<username>")
def user(username):
    searchedUser = User.query.filter_by(username=username).first()
    images = None
    # find all images posted by some user
    if searchedUser:
        images = searchedUser.images
    return render_template('viewimages.html', title="Images uploaded by: " + username, username=username, images=images)


@app.route("/search", methods=['GET', 'POST'])
def search():
    searchForm = Upload()
    images = []
    if searchForm.validate_on_submit():
        searchImg = pilImage.open(searchForm.image.data)
        # find hash of the image
        searchHash = imagehash.phash(searchImg)

        # find similar uploaded images
        # images are defined to be similar if the hamming distance, between 2 hashes is <= 10
        # the hamming distance needs to be modified/tweaked
        for img in Image.query.all():
            hashObject = imagehash.hex_to_hash(img.hash)
            if searchHash - hashObject <= 10:
                images.append(str(img))

    return render_template('search.html', title="Search", form=searchForm, images=images)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if user is already logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registerForm = Register()
    if registerForm.validate_on_submit():
        password = generate_password_hash(registerForm.password.data)
        newUser = User(username=registerForm.username.data, password=password)
        db.session.add(newUser)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registerForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    loginForm = Login()
    if loginForm.validate_on_submit():
        # log the user in
        loginUser = User.query.filter_by(username=loginForm.username.data).first()
        if loginUser and check_password_hash(loginUser.password, loginForm.password.data):
            login_user(loginUser, remember=loginForm.remember.data)
            redirect_page = request.args.get('next')
            if redirect_page:
                return redirect(url_for(redirect_page))
            else:
                return redirect(url_for('home'))

        flash('Invalid username or password!')
    return render_template('login.html', title='Login', form=loginForm)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = Upload()
    if form.validate_on_submit():
        uploadedImg = pilImage.open(form.image.data)
        # generate a hash from the image
        imgHash = str(imagehash.phash(uploadedImg))
        # check if image has been previously uploaded, it not save it to file system
        img = Image.query.filter_by(hash=imgHash).first()
        if not img:
            img = Image(hash=imgHash)
            db.session.add(img)
            path = os.path.join(app.root_path, 'static', imgHash+".png")
            uploadedImg.save(path)

        img.users.append(current_user)
        db.session.commit()
    return render_template('search.html', title="Upload", form=form)

