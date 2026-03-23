from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        try:
            user = auth_service.signup(username, email, password)
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Compte créé avec succès", "success")
            return redirect(url_for("prediction.predict"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        try:
            user = auth_service.login(username, password)
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Connexion réussie", "success")
            return redirect(url_for("prediction.predict"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Déconnexion réussie", "info")
    return redirect(url_for("main.index"))