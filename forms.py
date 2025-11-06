from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SermonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    preacher = StringField('Preacher')
    date_preached = DateField('Date Preached')
    description = TextAreaField('Description')
    audio_file = FileField('Audio File')
    video_file = FileField('Video File')
    notes = TextAreaField('Notes')
    submit = SubmitField('Upload')

class GalleryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    video = FileField('Video')
    submit = SubmitField('Upload')
