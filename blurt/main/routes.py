from flask import render_template, request, Blueprint
from blurt.models import Post
from blurt.users.utils import top_contributions

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page', 1, type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=posts, top_contributions=top_contributions())

@main.route('/about')
def about():
    return render_template('about.html',title='About Us', top_contributions=top_contributions())
