from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user
from forms import Login, Edit, Project


class Base(DeclarativeBase):
    pass


UPLOAD_FOLDER = '/home/aadi/Programming Files/Pycharm Projects/portfolio-site/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = 'sefoiIEFHUEJ983rHIUFhwrfh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolios.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)


class Projects(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    link_name: Mapped[str] = mapped_column(nullable=False)
    link_path: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(unique=False, nullable=False)


class Admin(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)


with app.app_context():
    db.create_all()

with app.app_context():
    user = Admin.query.filter_by(password='ugym67rhem').first()
    if user:
        user.password = "ugym67rhem"
    else:
        admin = Admin(password='ugym67rhem')
        db.session.add(admin)
        db.session.commit()

with (app.app_context()):
    @app.route("/")
    def home():
        login_status = current_user.is_authenticated
        all_posts = Projects.query.all()
        return render_template("index.html", posts=all_posts, status=login_status)


    @login_manager.user_loader
    def loader_user(user_id):
        return Admin.query.get(user_id)


    @app.route("/add", methods=['GET', 'POST'])
    def add():
        login_status = current_user.is_authenticated
        form = Project()
        if request.method == 'POST':
            project = Projects(
                name=form.name.data,
                description=form.description.data,
                link_name=form.link_name.data,
                link_path=form.link_path.data,
                content=form.content.data,
            )
            db.session.add(project)
            db.session.commit()
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Your entry has been added to the database')
            return redirect(url_for('home'))
        return render_template("add.html", form=form, status=login_status)


    @app.route("/project/<post_path>", methods=['POST', 'GET'])
    def show_post(post_path):
        login_status = current_user.is_authenticated
        name = Projects.query.filter_by(link_path=post_path).first().name
        content = Projects.query.filter_by(link_path=post_path).first().content
        return render_template('posts.html', path=post_path, name=name, content=content, status=login_status)


    @app.route("/project/edit/<post_path>", methods=['GET', 'POST'])
    def edit_post(post_path):
        login_status = current_user.is_authenticated
        post = Projects.query.filter_by(link_path=post_path).first()
        edit = Edit(obj=post)
        if request.method == 'POST':
            if edit.validate_on_submit():
                post.name = edit.name.data
                post.description = edit.description.data
                post.link_name = edit.link_name.data
                post.link_path = edit.link_path.data
                post.content = edit.content.data
            db.session.commit()
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for(f'show_post', post_path=post_path, status=login_status))
        return render_template("edit_post.html", form=edit, status=login_status)


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        login_status = current_user.is_authenticated
        form = Login()
        user = Admin.query.filter_by(id='1').first()
        if form.validate_on_submit():
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for('home'))
        return render_template('login.html', form=form, status=login_status)


    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
