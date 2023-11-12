from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import pyperclip

from forms import RegisterForm, LoginForm, AddPassword, EditPassword, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure.db'
db = SQLAlchemy()
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Define the model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    passwords = db.relationship('Passwords', backref='user')


class Passwords(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    website_name = db.Column(db.String(250), nullable=False)
    website_password = db.Column(db.String(250), nullable=False)
    website_password_hint = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("User Exists!")
            return redirect(url_for('register'))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=15)
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template("forms.html", form=form, registered=False, is_register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password!")
                return redirect(url_for('login'))
        else:
            flash("No user available!")
            return redirect(url_for('login'))
    return render_template("forms.html", form=form, registered=False, is_login=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_required
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    passwords = Passwords.query.filter_by(user_id=current_user.id).all()
    form = SearchForm()
    if form.validate_on_submit():
        valid_passwords = [password.website_name for password in passwords if check_password_hash(password.website_password, form.search.data)]
        if valid_passwords:
            flash(f"Password found in: {', '.join(valid_passwords)}")
            return redirect(url_for('dashboard'))
        else:
            flash("Error!")
            return redirect(url_for('dashboard'))
    return render_template("dashboard.html", registered=True, passwords=passwords, form=form)


@login_required
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_password():
    form = AddPassword(
        email=current_user.email,
    )
    if form.validate_on_submit():
        new_password_obj = Passwords(
            user_id=current_user.id,
            email=form.email.data,
            website_name=form.website_name.data,
            website_password=generate_password_hash(form.website_password.data, method='pbkdf2:sha256', salt_length=15),
            website_password_hint=form.website_password_hint.data
        )
        db.session.add(new_password_obj)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("forms.html", form=form, registered=True, is_add_password=True)


@app.route('/edit_password/<int:password_id>', methods=['GET', 'POST'])
@login_required
def edit_password(password_id):
    password_to_edit = db.get_or_404(Passwords, password_id)
    form = EditPassword(
        email=password_to_edit.email,
        website_name=password_to_edit.website_name,
        old_website_password=password_to_edit.website_password,
        website_password_hint=password_to_edit.website_password_hint
    )
    if form.validate_on_submit():
        password_to_edit.email = form.email.data
        password_to_edit.website_name = form.website_name.data
        password_to_edit.website_password = form.website_password.data
        password_to_edit.website_password_hint = form.website_password_hint.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("forms.html", form=form, registered=True, is_edit_password=True)


@app.route('/delete/<int:password_id>')
def delete_password(password_id):
    password_to_delete = db.get_or_404(Passwords, password_id)
    db.session.delete(password_to_delete)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/copy/<int:password_id>')
def copy_password(password_id):
    password_to_copy = db.get_or_404(Passwords, password_id)
    pyperclip.copy(password_to_copy.website_password)
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True, port=5002)
