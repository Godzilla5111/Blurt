import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from blurt import mail
from blurt.models import User, Post
from collections import Counter

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_file_name=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path, 'static/profile_pics', picture_file_name)

    #Resize image
    output_size = (125,125)
    i= Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    prev_picture = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return picture_file_name

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request', sender='blurt.assistance@gmail.com',recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
    {url_for('users.reset_token',token=token, _external=True)}
    If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

def top_contributions():
    all_users=User.query.all()
    top_contri=dict()
    for user in all_users:
        posts=Post.query.filter_by(author=user).all()
        top_contri[user.username]=len(posts)
    c=Counter(top_contri)
    return c.most_common(3)
