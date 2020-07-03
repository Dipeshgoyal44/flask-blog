from flask import render_template,request, Blueprint
from flaskblog.models import Post

main = Blueprint('main',__name__)


#Routes
@main.route('/')
@main.route('/home')
def home():
    #PAGINATION
    page = request.args.get('page',1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) #No. Of Posts Per Page
    return render_template('home.html', posts=posts)

#About
@main.route('/about')
def about():
    return render_template('about.html', title='About')  


