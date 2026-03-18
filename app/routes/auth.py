from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Role
from app.ldap_config import ldap_authenticate
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Вход выполнен.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        # LDAP fallback (если используете)
        ldap_info = ldap_authenticate(form.email.data, form.password.data)
        if ldap_info:
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                user = User(
                    username=ldap_info.get('username', form.email.data.split('@')[0]),
                    email=form.email.data,
                    active=True
                )
                user.set_password('')
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=True)
            flash('Вход через LDAP выполнен.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        client_role = Role.query.filter_by(name='client').first()
        if client_role:
            user.roles.append(client_role)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли.', 'info')
    return redirect(url_for('main.index'))