from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Appointment

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def profile():
    appointments = current_user.appointments.order_by(Appointment.date.desc()).all()
    return render_template('profile.html', appointments=appointments)