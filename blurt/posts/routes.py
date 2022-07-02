from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blurt import db
from blurt.models import Post
from blurt.posts.forms import PostForm
from blurt.users.utils import top_contributions

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form, top_contributions=top_contributions())

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    admin=0
    if not current_user.is_anonymous:
        if current_user.username=='Admin':
            admin=1
            print('Admin is online!')
    return render_template('post.html', title=post.title, post=post, admin=admin, top_contributions=top_contributions())

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if(post.author!=current_user and current_user.username!='Admin'):
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your Post has been updated successfully!', category='info')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', top_contributions=top_contributions())

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if not current_user.is_anonymous:
        if(post.author!=current_user and current_user.username!='Admin'):
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted succesfully!', category='success')
        return redirect(url_for('main.home'))
