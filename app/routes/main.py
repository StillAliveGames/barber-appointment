from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.forms import AppointmentForm
from app.models import Master, Service, Appointment

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = AppointmentForm()
    form.master.choices = [(m.id, m.user.username) for m in Master.query.all()]
    form.service.choices = [(s.id, f"{s.name} - {s.price} руб.") for s in Service.query.all()]

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Чтобы записаться, необходимо войти.', 'warning')
            return redirect(url_for('auth.login'))

        existing = Appointment.query.filter_by(
            master_id=form.master.data,
            date=form.date.data,
            time=form.time.data
        ).first()
        if existing:
            flash('Это время уже занято.', 'danger')
            return redirect(url_for('main.index'))

        appointment = Appointment(
            user_id=current_user.id,
            master_id=form.master.data,
            service_id=form.service.data,
            date=form.date.data,
            time=form.time.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Запись успешно создана!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('index.html', form=form)