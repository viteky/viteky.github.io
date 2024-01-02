from os import remove
from credits import app, db, bcrypt
from credits.models import User, Claim, Item
from credits.helpers import save_picture
from credits.forms import registrationForm, loginForm, updateAccountForm, newClaimForm, adminControlForm
from flask import redirect, render_template, request, session, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/")
@login_required
def index():
    claims = Claim.query.all()
    user = User.query.filter_by(id=current_user.id).first()

    return render_template("index.html", claims=claims, user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = loginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                flash(f"Successfully Logged In!", "success")
                return redirect(next_page) if next_page else redirect(url_for("index"))
            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = registrationForm()
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data, 
                    password=hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)
    
@app.route("/logout")
def logout():
    """Log user out"""
    logout_user()
    return redirect(url_for("login"))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Account overview page"""
    form = updateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            if current_user.image_file != "default_user.jpg":
                remove(app.root_path + "/static/profile_pics/" + current_user.image_file)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form)


@app.route("/claim/<int:claim>", methods=["GET", "POST"])
@login_required
def claim():
    claims = Claim.query.filter_by(id=claim)
    return render_template("claim.html", claims=claims)



@app.route("/claim/new", methods=["GET", "POST"])
@login_required
def new_claim():
    """New Claim Form"""
    form = newClaimForm()
    if form.validate_on_submit():
        claim = Claim(customer_id=form.customer_id.data, invoice_num=form.invoice_num.data,
                      invoice_date=form.invoice_date.data, run_num=form.run_num.data,
                      notify_date=form.notify_date.data, driver=form.driver.data,
                      notes=form.notes.data, user_id=current_user.id)
        db.session.add(claim)
        db.session.commit()
        flash(f"New claim for invoice {form.invoice_num.data} created!")
    return render_template("claim_form.html", form=form)
        

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """Admin control panel"""
    users = User.query.all()
    form = adminControlForm()
    

    if form.validate_on_submit():
        db.session.commit()
        flash("User updated")
    
    return render_template("admin.html", users=users, form=form)


