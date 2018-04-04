from flask import Flask, render_template,redirect, url_for
from flask_mongoengine import MongoEngine
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = { 
    'db': 'users' 
}
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
db = MongoEngine(app)

class User(db.Document):
    name = db.StringField(max_length = 50)
    email = db.StringField(max_length = 50)
    group = db.ListField()
    meta = {'users': 'User'}

class RegistrationForm(FlaskForm):
    username = StringField('Name',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=3)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = StringField('password', [validators.Length(min=6, max=35)])
    confirm = PasswordField('Repeat Password')


@app.route("/")
def index():
   return render_template('index.html')


@app.route("/login")
def login():
   return render_template('login.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template('register.html', form=form)
    user = User(name=form.username.data,email=form.email.data,)
    user.save()
    return render_template('login.html')

@app.route("/camera")
def camera():
   return render_template('camera.html')

@app.route("/home")
def home():
   return render_template('home.html')

@app.route("/test")
def test():
   users = User.objects
   for user in users:
        print(user.name)
   return render_template('test.html', users=users)

if __name__=='__main__':
    app.run(debug=True)