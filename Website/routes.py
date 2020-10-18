from datetime import datetime
from Website import app, db
from Website.forms import RegistrationForm, ConfirmData, YesandNoForm
from Website.models import User, DataRegistered
from flask import render_template, url_for, flash, redirect, request


date_now = datetime.now()


@app.route("/", methods=["GET", "POST"])
@app.route("/delete_all", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = ConfirmData()
    db.create_all()
    page = request.args.get("page", 1, type=int)
    user = User.query.order_by(User.time_check.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", user=user, date=date_now, form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User(
            address=form.address.data,
            first=form.first.data.strip(),
            last=form.last.data.strip(),
            age=form.age.data,
            email=form.email.data,
            phone=form.phone.data,
        )

        phone_check = User.query.filter_by(phone=form.phone.data).first()
        email_check = User.query.filter_by(email=form.email.data).first()
        if phone_check and email_check:
            return redirect(
                url_for(
                    "customer_confirm", phone_no=phone_check.phone, email=email_check
                )
            )
        if phone_check:
            return redirect(url_for("customer_confirm", phone_no=phone_check.phone))
        if email_check:
            return redirect(url_for("customer_confirm_email", email=email_check.email))

        else:
            db.session.add(user)
            db.session.commit()
            user_check = User.query.filter_by(phone=user.phone).first()
            time_check = DataRegistered(author=user_check)
            db.session.add(time_check)
            db.session.commit()
            flash(f"Your account has been created!", "success")
            return redirect(url_for("home"))
    phone_check = User.query.filter_by(phone=form.phone.data).first()

    return render_template("register.html", title="Register", form=form, date=date_now)


@app.route("/customer/<int:phone>")
def customer(phone):
    user = User.query.filter_by(phone=phone).first()
    user_check = user.data
    image_file = url_for("static", filename="profile_pics/" + user.image_file)
    return render_template(
        "customer.html",
        user=user,
        date=date_now,
        image_file=image_file,
        user_check=user_check,
    )


@app.route("/confirm_data", methods=["GET", "POST"])
def confirm_data():
    form = RegistrationForm()
    phone = User.query.filter_by(phone=form.phone.data).first()
    if phone and form.submit.data:
        time_check = DataRegistered(author=phone)
        db.session.add(time_check)
        db.session.commit()
        flash(f"Confirmed data! Please enjoy your visit", "success")
        return redirect(url_for("home"))
    else:
        flash(f"No email and phone no. detected. Please Register first!", "danger")
        return redirect(url_for("register"))
    return render_template("confirm_data.html", date=date_now, form=form)


@app.route("/customer", methods=["GET", "POST"])
def delete_all():
    form = ConfirmData()
    if form.submit.data:
        if form.email.data == "admin" and form.password.data == "pass123":
            db.session.query(User).delete()
            db.session.query(DataRegistered).delete()
            db.session.commit()
            flash(f"All data has been deleted!", "info")
            return redirect(url_for("home"))
        else:
            flash("User authentication invalid", "danger")
            return redirect(url_for("home"))

    return render_template("admin.html", date=date_now, form=ConfirmData())


@app.route("/customer_confirm/<phone_no>", methods=["GET", "POST"])
def customer_confirm(phone_no):
    image_file = url_for("static", filename="profile_pics/" + "default.jpg")
    phone_check = User.query.filter_by(phone=phone_no).first()
    form = YesandNoForm()
    if form.No.data:
        flash("Please register again!", "danger")
        return redirect(url_for("register"))
    if form.Yes.data:
        phone_check = User.query.filter_by(phone=phone_no).first()
        time_check = DataRegistered(author=phone_check)
        db.session.add(time_check)
        db.session.commit()
        flash(f"Data is successfully recorded. Please enjoy your visit!", "success")
        return redirect(url_for("home"))

    else:
        return render_template(
            "customer_confirm.html",
            title="Customer Info",
            user=phone_check,
            form=form,
            date=date_now,
            image_file=image_file,
        )


@app.route("/customer_confirm_email/<email>", methods=["GET", "POST"])
def customer_confirm_email(email):
    image_file = url_for("static", filename="profile_pics/" + "default.jpg")
    email_check = User.query.filter_by(email=email).first()
    form = YesandNoForm()
    return render_template(
        "customer_confirm.html",
        title="Customer Info",
        user=email_check,
        form=form,
        date=date_now,
        image_file=image_file,
    )
