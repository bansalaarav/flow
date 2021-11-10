from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^AAAAAAAAAAAAAAAAAAA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flow.db'

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'flowtable'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))


@app.route("/")
def index():
    if session.get("logged-in"):
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html")

@app.route("/terms-of-use/")
def terms_of_use():
    return render_template("term-of-use.html")

@app.route("/privacy-policy/")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/blog/")
def blog():
    return render_template("blog-page.html")

@app.route("/dashboard/")
def dashboard():
    if session.get("logged-in"):
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/quizzes/")
def quizzes():
    if session.get("logged-in"):
        return render_template("quizzes.html")
    else:
        return redirect(url_for("login"))

@app.route("/blog/<variable>/")
def blog_pages(variable):
    if variable == "history-of-drone-tech":
        return render_template("blogs/blog-1.html")
    elif variable == "how-do-drones-work":
        return render_template("blogs/blog-2.html")
    elif variable == "drones-and-covid-19":
        return render_template("blogs/blog-3.html")

    return redirect(url_for("blog"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):

                session["logged-in"] = True

                session['email'] = user.email

                session['first_name'] = user.first_name
                flash('Login successful!')
                print("login successful")
                return redirect(url_for("dashboard"))
            else:
                flash('Incorrect password!')
                return redirect(url_for("login"))
        flash('Email does not exist!')
        print("Email does not exist!")
        return redirect(url_for("login"))
    if session.get("logged-in"):
        print("logged in")
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")


@app.route('/logout/')
def logout():
    session["logged-in"] = False
    flash("Logged out successfully!")
    return redirect(url_for('index'))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        user = User.query.filter_by(email=email).first()

        if not user:

            if password == confirm_password:
                hashed_password = generate_password_hash(password, method='sha256')
                new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful!")

                session["logged-in"] = True

                session['email'] = new_user.email

                session['first_name'] = new_user.first_name
                print("reg success")
                return redirect(url_for("dashboard"))
            else:
                flash("Passwords do not match!")
                return redirect(url_for("register"))
        else:
            flash("An account with that email already exists!")
            return redirect(url_for("register"))
    if session.get("logged-in"):
        print("reg logged in")
        return redirect(url_for("dashboard"))

    return render_template("register.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
