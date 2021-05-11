from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, SignInForm, FeedBackForm, DeleteForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def enter():
    
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


###############################################################################
#####                            USER PAGES                 ##############


##### Register ######
@app.route('/register', methods=["GET", "POST"])
def register_user():
    form=RegisterForm()
    
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data 
        first_name=form.first_name.data    
        last_name=form.last_name.data   
        
        new_user=User.register(username, password, email, first_name, last_name)
        
        db.session.add(new_user)
        
        try:
            db.session.commit()
            
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            
            return render_template('register.html', form=form)
        session['username']=new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f"/users/{new_user.username}")
    
    return render_template('register.html', form=form)

###### Login #####

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form=SignInForm()
    
    if form.validate_on_submit():
        email=form.email.data
        
        password = form.password.data

        user= User.authenticate(email, password)
        
        if user:
           flash('Welcome!!', "success") 
           session['username']=user.username
           return redirect(f"/users/{user.username}")
        else:
            form.email.errors = ['Invalid username/password.']
            
    return render_template('login.html', form=form)


##### home ####
"""
@app.route('/home')
def home():
    return render_template('home.html')

"""

##### logout #####


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')

############################################################################
######################   FEEDBACKS #################################

@app.route('/users/<username>')
def feedbacks_list(username):
    feedbacks_elements= Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('home.html', feedbacks=feedbacks_elements)



@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    

    form = FeedBackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("new_feedback.html", form=form)
    
    
    



@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")



##########################################################################
#################           USERS       ##################################
"""
@app.route('/users')
def users_list():
    userses=User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list_users.html', users=userses)
"""
@app.route('/users/<username>/show')
def show_user(username):
    one_user=User.query.get_or_404(username)
    return render_template('show_user.html', user=one_user)




@app.route('/users/<username>/edit', methods=["GET","POST"])
def user_edit(username):
    form=RegisterForm()
    user= User.query.get_or_404(username)
    if form.validate_on_submit():
        user.username=form.username.data
        user.email=form.email.data  
        user.first_name=form.first_name.data 
        user.last_name=form.last_name.data  
         
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('edit_user.html', form=form)
        session['username'] = user.username
        flash('Welcome! Successfully Edited Your Account!', "success")
        return redirect('/users')

    return render_template('edit_user.html', form=form)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    user=User.query.get_or_404(username)
    
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('Account Deleted!!', "info")
    return redirect('/')


       
         