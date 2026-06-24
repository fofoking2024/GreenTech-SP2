from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
import models
from datetime import date, datetime
from sqlalchemy import func

user_bp = Blueprint('user', __name__)

@user_bp.route('/home')
def user_home():
    if 'user_id' not in session or session.get('role') != 'individual':
        return redirect(url_for('auth.user_login'))

    user_id = session['user_id']
    total_orders = models.Request.query.filter_by(user_id=user_id).count()

    devices_recycled = db.session.query(
        func.sum(models.Device.quantity)
    ).join(models.Request).filter(
        models.Request.user_id == user_id,
        models.Request.status == 'Recycled'
    ).scalar() or 0

    completed_orders = models.Request.query.filter_by(
        user_id=user_id,
        status='Recycled'
    ).count()

    return render_template(
        'user-portal/user-home.html',
        username=session['name'],
        total_orders=total_orders,
        devices_recycled=devices_recycled,
        completed_orders=completed_orders
    )

@user_bp.route('/order/devices', methods=['GET', 'POST'])
def device_registration():
    if 'user_id' not in session or session.get('role') != 'individual':
        return redirect(url_for('auth.user_login'))

    companies = models.Company.query.all()
    selected_company_id = request.args.get('company_id', type=int)
    points = []
    error = None

    if selected_company_id:
        points = models.CollectionPoint.query.filter(
            models.CollectionPoint.company_id == selected_company_id,
            models.CollectionPoint.isActive == True,
            models.CollectionPoint.map_url.isnot(None)
        ).all()

    if request.method == 'POST':
        company_id = request.form.get('company_id', type=int)
        point_id = request.form.get('point_id', type=int)
        device_types = request.form.getlist('device_type[]')
        quantities = request.form.getlist('quantity[]')
        conditions = request.form.getlist('condition[]')

        if company_id:
            points = models.CollectionPoint.query.filter(
                models.CollectionPoint.company_id == company_id,
                models.CollectionPoint.isActive == True,
                models.CollectionPoint.map_url.isnot(None)
            ).all()

        if not company_id or not point_id:
            error = 'Please select a company and collection point.'
        elif not device_types or not quantities:
            error = 'Please add at least one device.'
        else:
            point = models.CollectionPoint.query.filter(
                models.CollectionPoint.point_id == point_id,
                models.CollectionPoint.company_id == company_id,
                models.CollectionPoint.isActive == True
            ).first()

            if not point:
                error = 'Selected collection point is not valid.'
            else:
                devices_to_add = []
                total_items = min(len(device_types), len(quantities), len(conditions))

                for i in range(total_items):
                    dtype = (device_types[i] or '').strip()
                    qty_raw = (quantities[i] or '').strip()
                    cond = (conditions[i] or '').strip()

                    if not dtype or not qty_raw:
                        continue
                    try:
                        qty = int(qty_raw)
                        if qty < 1: continue
                    except ValueError: continue
                    devices_to_add.append((dtype, qty, cond if cond else None))

                if not devices_to_add:
                    error = 'Please enter valid device details.'
                else:
                    current_date = date.today()
                    start_date = date(current_date.year, current_date.month, 1)
                    if current_date.month == 12:
                        end_date = date(current_date.year + 1, 1, 1)
                    else:
                        end_date = date(current_date.year, current_date.month + 1, 1)

                    requests_count = models.Request.query.filter(
                        models.Request.user_id == session['user_id'],
                        models.Request.request_date >= start_date,
                        models.Request.request_date < end_date
                    ).count()

                    if requests_count >= 10:
                        flash('You have reached the maximum requests for this month (10).', 'error')
                        return redirect(url_for('user.request_history'))

                    new_req = models.Request(
                        user_id=session['user_id'],
                        company_id=company_id,
                        point_id=point_id,
                        request_date=date.today(),
                        status='Received'
                    )
                    db.session.add(new_req)
                    db.session.flush()

                    db.session.add(models.RequestHistory(
                        request_id=new_req.request_id,
                        status='Received',
                        updated_at=datetime.now()
                    ))

                    for dtype, qty, cond in devices_to_add:
                        db.session.add(models.Device(
                            type=dtype,
                            quantity=qty,
                            condition=cond,
                            request_id=new_req.request_id
                        ))

                    db.session.commit()
                    return redirect(url_for('user.request_history'))

        selected_company_id = company_id

    return render_template(
        'user-portal/device-registration.html',
        companies=companies,
        points=points,
        selected_company_id=selected_company_id,
        error=error
    )

@user_bp.route('/history')
def request_history():
    if 'user_id' not in session or session.get('role') != 'individual':
        return redirect(url_for('auth.user_login'))

    requests_list = (
        db.session.query(models.Request, models.Company, models.CollectionPoint)
        .join(models.Company, models.Request.company_id == models.Company.company_id)
        .join(models.CollectionPoint, models.Request.point_id == models.CollectionPoint.point_id)
        .filter(models.Request.user_id == session['user_id'])
        .order_by(models.Request.request_id.desc())
        .all()
    )

    orders = []
    for req, company, point in requests_list:
        device_count = db.session.query(
            func.sum(models.Device.quantity)
        ).filter(models.Device.request_id == req.request_id).scalar() or 0
        
        last_status = models.RequestHistory.query.filter_by(
            request_id=req.request_id
        ).order_by(
            models.RequestHistory.updated_at.desc()
        ).first()

        orders.append({
            'id': req.request_id,
            'status': last_status.status.lower().replace(' ', '-') if last_status else req.status.lower().replace(' ', '-'),
            'date': req.request_date.strftime('%B %d, %Y') if req.request_date else '',
            'device_count': device_count,
            'collection_point': point.location,
            'company_name': company.name
        })

    return render_template('user-portal/request-history.html', orders=orders)

@user_bp.route('/history/<int:order_id>')
def request_details(order_id):
    if 'user_id' not in session or session.get('role') != 'individual':
        return redirect(url_for('auth.user_login'))

    req = models.Request.query.get_or_404(order_id)
    if req.user_id != session['user_id']:
        return redirect(url_for('user.request_history'))

    point = models.CollectionPoint.query.get(req.point_id)
    devices = models.Device.query.filter_by(request_id=req.request_id).all()
    history = models.RequestHistory.query.filter_by(request_id=req.request_id).order_by(models.RequestHistory.updated_at.desc()).all()
    company = models.Company.query.get(req.company_id)

    order = {
        'id': req.request_id,
        'status': req.status.lower().replace(' ', '-'),
        'date': req.request_date.strftime('%B %d, %Y') if req.request_date else '',
        'collection_point': point.location if point else '',
        'collection_address': point.map_url if point else '',
        'collection_hours': '',
        'collection_contact': ''
    }

    return render_template(
        'user-portal/request-details.html',
        order=order,
        devices=devices,
        history=history,
        company_name=company.name 
    )
