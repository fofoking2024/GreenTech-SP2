from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import models
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@auth_bp.route('/user/logout')
def user_logout():
    session.clear()
    return redirect(url_for('index'))

@auth_bp.route('/company/logout')
def company_logout():
    session.clear()
    return redirect(url_for('index'))

@auth_bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = models.User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            error = 'Invalid email or password.'
        elif user.role != 'individual':
            error = 'This account is not a user account.'
        else:
            session['user_id'] = user.user_id
            session['role'] = user.role
            session['name'] = user.name
            session['email'] = user.email
            return redirect(url_for('user.user_home'))
    return render_template('user-portal/user-login.html', error=error)

@auth_bp.route('/user/register', methods=['GET', 'POST'])
def user_reg():
    error = None
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        phone = (request.form.get('phone') or '').strip()

        # Validate phone: must be +967 followed by exactly 9 digits
        if phone and not (phone.startswith('+967') and len(phone) == 13 and phone[4:].isdigit()):
            error = 'Phone number must be +967 followed by 9 digits (e.g. +967777688809).'
        elif not name or not email or not password:
            error = 'Please fill in all required fields.'
        elif '@' not in email or '.' not in email:
            error = 'Invalid email address.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        else:
            existing = models.User.query.filter_by(email=email).first()
            if existing:
                error = 'This email is already registered.'
            else:
                try:
                    hashed = generate_password_hash(password)
                    new_user = models.User(
                        name=name,
                        email=email,
                        password=hashed,
                        phone=phone if phone else None,
                        role='individual'
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('auth.user_login'))
                except IntegrityError:
                    db.session.rollback()
                    error = 'An account with this email already exists.'
                except Exception:
                    db.session.rollback()
                    error = 'An unexpected error occurred. Please try again.'
    return render_template('user-portal/user-reg.html', error=error)

@auth_bp.route('/company/login', methods=['GET', 'POST'])
def company_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = models.User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            error = 'Invalid email or password.'
        elif user.role != 'company':
            error = 'This account is not a company account.'
        else:
            company = models.Company.query.filter_by(email=email).first()
            if company:
                session['company_id'] = company.company_id
            session['user_id'] = user.user_id
            session['role'] = user.role
            session['name'] = user.name
            session['email'] = user.email
            return redirect(url_for('company.company_home'))
    return render_template('company-portal/company-login.html', error=error)

@auth_bp.route('/company/register', methods=['GET', 'POST'])
def company_reg():
    error = None
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        registration_no = (request.form.get('registration_no') or '').strip()

        if not name or not email or not password or not registration_no:
            error = 'Please fill in all required fields.'
        elif '@' not in email or '.' not in email:
            error = 'Invalid email address.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif not registration_no.isdigit():
            error = 'Registration number must be digits only.'
        else:
            existing_user = models.User.query.filter_by(email=email).first()
            existing_company = models.Company.query.filter_by(registration_no=registration_no).first()

            if existing_user:
                error = 'This email is already registered.'
            elif existing_company:
                error = 'This registration number is already in use.'
            else:
                try:
                    hashed = generate_password_hash(password)
                    new_user = models.User(
                        name=name,
                        email=email,
                        password=hashed,
                        phone=None,
                        role='company'
                    )
                    db.session.add(new_user)
                    db.session.flush()

                    new_company = models.Company(
                        name=name,
                        registration_no=registration_no,
                        email=email,
                        password=hashed
                    )
                    db.session.add(new_company)
                    db.session.commit()
                    return redirect(url_for('auth.company_login'))
                except IntegrityError:
                    db.session.rollback()
                    error = 'A conflict occurred. Please check your details.'
                except Exception:
                    db.session.rollback()
                    error = 'An unexpected error occurred. Please try again.'
    return render_template('company-portal/company-reg.html', error=error)
