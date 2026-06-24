from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import models
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__)

# Simple hardcoded admin credentials
ADMIN_EMAIL = 'admin@greentech.com'
ADMIN_PASSWORD_HASH = generate_password_hash('admin123')

@admin_bp.route('/admin')
def admin_index():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        if email == ADMIN_EMAIL and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            session['admin_email'] = email
            return redirect(url_for('admin.admin_dashboard'))
        else:
            error = 'Invalid admin email or password.'

    return render_template('admin/admin-login.html', error=error)

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    # Get all users (individual)
    users = models.User.query.filter_by(role='individual').all()

    # Get all companies with their user info
    companies = (
        db.session.query(models.Company, models.User)
        .join(models.User, models.Company.email == models.User.email)
        .all()
    )

    return render_template('admin/dashboard.html', users=users, companies=companies)

@admin_bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    user = models.User.query.get_or_404(user_id)
    if user.role != 'individual':
        flash('This route is only for individual users.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

    try:
        # Delete related requests and their devices/history first
        requests = models.Request.query.filter_by(user_id=user_id).all()
        for req in requests:
            models.Device.query.filter_by(request_id=req.request_id).delete()
            models.RequestHistory.query.filter_by(request_id=req.request_id).delete()
            db.session.delete(req)

        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user.name}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/delete-company/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    company = models.Company.query.get_or_404(company_id)
    user = models.User.query.filter_by(email=company.email).first()

    try:
        # Delete related collection points
        points = models.CollectionPoint.query.filter_by(company_id=company_id).all()
        for point in points:
            # Delete requests linked to this point
            requests = models.Request.query.filter_by(point_id=point.point_id).all()
            for req in requests:
                models.Device.query.filter_by(request_id=req.request_id).delete()
                models.RequestHistory.query.filter_by(request_id=req.request_id).delete()
                db.session.delete(req)
            db.session.delete(point)

        # Delete any remaining requests linked to this company
        requests = models.Request.query.filter_by(company_id=company_id).all()
        for req in requests:
            models.Device.query.filter_by(request_id=req.request_id).delete()
