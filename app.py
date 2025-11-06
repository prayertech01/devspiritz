from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from config import Config
from models import db, User, Sermon, GalleryItem
from forms import LoginForm, SermonForm, GalleryForm
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    sermons = Sermon.query.order_by(Sermon.date_preached.desc()).limit(5).all()
    gallery = GalleryItem.query.order_by(GalleryItem.uploaded_at.desc()).limit(8).all()
    return render_template('home.html', sermons=sermons, gallery=gallery)

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard') if user.is_admin else url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    sermons = Sermon.query.order_by(Sermon.date_preached.desc()).all()
    gallery = GalleryItem.query.order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('dashboard.html', sermons=sermons, gallery=gallery)

@app.route('/admin/upload-sermon/', methods=['GET','POST'])
@login_required
def upload_sermon():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = SermonForm()
    if form.validate_on_submit():
        audio_filename = secure_filename(form.audio_file.data.filename) if form.audio_file.data else None
        video_filename = secure_filename(form.video_file.data.filename) if form.video_file.data else None
        if audio_filename:
            form.audio_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'sermons', audio_filename))
        if video_filename:
            form.video_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'sermons', video_filename))
        sermon = Sermon(title=form.title.data, preacher=form.preacher.data, date_preached=form.date_preached.data or datetime.utcnow(), description=form.description.data, audio_file=audio_filename, video_file=video_filename, notes=form.notes.data)
        db.session.add(sermon)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('upload_sermon.html', form=form)

@app.route('/admin/gallery/', methods=['GET','POST'])
@login_required
def manage_gallery():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = GalleryForm()
    if form.validate_on_submit():
        image_filename = secure_filename(form.image.data.filename) if form.image.data else None
        video_filename = secure_filename(form.video.data.filename) if form.video.data else None
        if image_filename:
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery', image_filename))
        if video_filename:
            form.video.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery', video_filename))
        item = GalleryItem(title=form.title.data, image=image_filename, video=video_filename)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('manage_gallery'))
    items = GalleryItem.query.order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('gallery.html', form=form, items=items)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@naubcf.com', password=generate_password_hash('admin123'), is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)
