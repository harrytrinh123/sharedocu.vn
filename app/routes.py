import os
from flask import render_template, request, redirect, url_for, session, flash
from app import app, db, bcrypt
from app.models import *
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return USER.query.get(int(id))

# ================== Authentication Hoang =====================
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = USER.query.filter_by(
            UserName=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.password.data)
    print(form.username.data)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = USER(UserName=form.username.data, Password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = USER.query.filter_by(UserName=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.Password, form.password.data):
                login_user(user)
                # Add username to session
                session['userid'] = user.id
                return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#=================== End Authentication Hoang =================

# ================== PRODUCT Hoang ============================
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/productmanage')
@login_required
def productmanage():
    # Get username from session
    user_id = session.get('userid')
    entries = PRODUCT.query.filter_by(UserId=int(user_id)).all()
    return render_template('productmanage.html', entries=entries)

@app.route('/add', methods=['POST'])
@login_required
def add():
    user_id = session.get('userid')
    print(user_id)
    if request.method == 'POST':
        form = request.form
        name = form.get('name')
        description = form.get('description')
        # xu ly file
        image = request.files["img_name"]
        if image.filename == "":
            flash('Please Upload Image file', "danger")
            return redirect(request.url)
        if allowed_image(image.filename) and (not name or description):
            filename = secure_filename(image.filename)
            try:
                entry = PRODUCT(Name = name, Description = description, ImageUrl = filename, Status=1, Surcharge=0, UserId=user_id)
                db.session.add(entry)
                db.session.commit()
                image.save(app.config["IMAGE_UPLOADS"] +'\\'+ filename)
                flash('File upload Successfully !', "success")
                return redirect('/productmanage')
            except IntegrityError as e:
                flash('Something went wrong please try again later', "danger")
                return redirect(request.url)        
    return "Something went wrong"

@app.route('/update/<int:id>')
@login_required
def updateRoute(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "Something went wrong"

@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            form = request.form
            name = form.get('name')
            description = form.get('description')
            entry.Name = name
            entry.Description = description
            db.session.commit()
        return redirect('/productmanage')

    return "Something went wrong"



@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/productmanage')

    return "Something went wrong"

@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = PRODUCT.query.get(id)
        if entry:
            if entry.Status==1:
                entry.Status = 2
            elif entry.Status==2:
                entry.Status = 3
            else:
                entry.Status = 1
            db.session.commit()
        return redirect('/productmanage')

    return "Something went wrong"
# ================================= END PRODUCT HOANG ======================================

@app.route('/')
@app.route('/index')
def index():
    list_product = PRODUCT.query.all()
    return render_template('index.html', list_product = list_product)




@app.route('/productdetail/<product_id>')
def productdetail(product_id):
    product = PRODUCT.query.get(product_id)  
    userId  = product.UserId
    user = USER.query.get(userId)
    return render_template('productdetail.html', product = product, user = user)

if __name__ == '__main__':
    app.run(debug=True)
    print('test')
    
