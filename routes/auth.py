from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from extensions import db
from models.user import User
from datetime import datetime


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':

        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()

        college = request.form.get('college', '').strip()
        degree = request.form.get('degree', '').strip()
        branch = request.form.get('branch', '').strip()
        current_year = request.form.get('current_year', '').strip()
        cgpa = request.form.get('cgpa', '').strip()
        graduation_year = request.form.get('graduation_year', '').strip()

        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Required field validation
        if not name or not email or not phone or not college:
            flash(
                'Please fill in all required student details.',
                'error'
            )
            return render_template('auth/register.html')

        # Phone validation
        phone_digits = ''.join(
            character for character in phone
            if character.isdigit()
        )

        if len(phone_digits) != 10:
            flash(
                'Please enter a valid 10-digit mobile number.',
                'error'
            )
            return render_template('auth/register.html')

        # Password validation
        if len(password) < 6:
            flash(
                'Password must contain at least 6 characters.',
                'error'
            )
            return render_template('auth/register.html')

        if password != confirm_password:
            flash(
                'Passwords do not match.',
                'error'
            )
            return render_template('auth/register.html')

        # Duplicate email check
        if User.query.filter_by(email=email).first():
            flash(
                'An account with this email already exists.',
                'error'
            )
            return render_template('auth/register.html')

        # Create user
        user = User(
            name=name,
            email=email,
            phone=phone_digits,
            college=college,
            degree=degree,
            branch=branch,
            current_year=current_year,
            cgpa=cgpa,
            graduation_year=graduation_year,
            role='student',
            xp=0,
            streak=0,
            last_active=datetime.utcnow()
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Login immediately after registration
        login_user(user)

        flash(
            'Account created successfully! Welcome to PlacePrep.',
            'success'
        )

        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':

        email = request.form.get(
            'email',
            ''
        ).strip().lower()

        password = request.form.get(
            'password',
            ''
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(password):

            user.last_active = datetime.utcnow()

            db.session.commit()

            login_user(
                user,
                remember=True
            )

            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)

            if user.role == 'admin':
                return redirect(
                    url_for('admin.index')
                )

            return redirect(
                url_for('dashboard.index')
            )

        flash(
            'Invalid email or password.',
            'error'
        )

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():

    logout_user()

    return redirect(
        url_for('main.home')
    )