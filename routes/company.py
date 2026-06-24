from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
import models
from datetime import datetime
from sqlalchemy import func
from utils.helpers import is_valid_url

company_bp = Blueprint('company', __name__)

@company_bp.route('/company')
def company_home():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    new_requests = models.Request.query.filter_by(company_id=company.company_id, status='Received').count()
    total_orders = models.Request.query.filter_by(company_id=company.company_id).count()
    collection_points_count = models.CollectionPoint.query.filter_by(company_id=company.company_id, isActive=True).count()
    devices_recycled = db.session.query(func.sum(models.Device.quantity)).join(models.Request).filter(
        models.Request.company_id == company.company_id,
        models.Request.status == 'Recycled'
    ).scalar() or 0

    return render_template(
        'company-portal/company-home.html',
        company_name=company.name,
        new_requests=new_requests,
        total_orders=total_orders,
        collection_points=collection_points_count,
        devices_recycled=devices_recycled
    )

@company_bp.route('/company/requests')
def recycling_requests():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    requests_list = (
        db.session.query(models.Request, models.User, models.CollectionPoint)
        .join(models.User, models.Request.user_id == models.User.user_id)
        .join(models.CollectionPoint, models.Request.point_id == models.CollectionPoint.point_id)
        .filter(models.Request.company_id == company.company_id)
        .order_by(models.Request.request_id.desc())
        .all()
    )

    requests = []
    for req, user, point in requests_list:
        device_count = db.session.query(func.sum(models.Device.quantity)).filter(models.Device.request_id == req.request_id).scalar() or 0
        requests.append({
            'id': req.request_id,
            'status': req.status.lower().replace(' ', '-'),
            'date': req.request_date.strftime('%B %d, %Y') if req.request_date else '',
            'user_name': user.name,
            'device_count': device_count,
            'collection_point': point.location
        })
    return render_template('company-portal/manage-requests.html', requests=requests)

@company_bp.route('/company/requests/<int:request_id>')
def request_details_company(request_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    req = models.Request.query.get_or_404(request_id)
    if req.company_id != company.company_id:
        return redirect(url_for('company.recycling_requests'))

    user = models.User.query.get(req.user_id)
    point = models.CollectionPoint.query.get(req.point_id)
    devices = models.Device.query.filter_by(request_id=req.request_id).all()

    request_obj = {
        'id': req.request_id,
        'status': req.status.lower().replace(' ', '-'),
        'date': req.request_date.strftime('%B %d, %Y') if req.request_date else '',
        'user_name': user.name if user else '',
        'user_email': user.email if user else '',
        'user_phone': user.phone if user else '',
        'collection_point': point.location if point else '',
        'collection_address': point.map_url if point else ''
    }
    return render_template('company-portal/request-details-company.html', request_data=request_obj, devices=devices)

@company_bp.route('/company/requests/<int:request_id>/update-status', methods=['POST'])
def update_request_status(request_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    req = models.Request.query.get_or_404(request_id)
    if req.company_id != company.company_id:
        return redirect(url_for('company.recycling_requests'))

    status_order = {'Received': 1, 'Under Recycling': 2, 'Recycled': 3}
    new_status = request.form.get('new_status')
    status_map = {'received': 'Received', 'under-recycling': 'Under Recycling', 'recycled': 'Recycled'}
    mapped_status = status_map.get(new_status)

    if not mapped_status:
        flash('Invalid status.', 'error')
        return redirect(url_for('company.request_details_company', request_id=request_id))

    if status_order.get(mapped_status, 0) <= status_order.get(req.status, 0):
        flash('Cannot go back to a previous status.', 'error')
        return redirect(url_for('company.request_details_company', request_id=request_id))

    req.status = mapped_status
    db.session.add(models.RequestHistory(request_id=req.request_id, status=mapped_status, updated_at=datetime.now()))
    db.session.commit()
    flash('Status updated successfully.', 'success')
    return redirect(url_for('company.request_details_company', request_id=request_id))

@company_bp.route('/company/collection-points')
def collection_points():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    rows = (
        db.session.query(models.CollectionPoint, func.count(models.Request.request_id).label('requests_count'))
        .outerjoin(models.Request, models.Request.point_id == models.CollectionPoint.point_id)
        .filter(models.CollectionPoint.company_id == company.company_id)
        .group_by(models.CollectionPoint.point_id)
        .order_by(models.CollectionPoint.point_id.desc())
        .all()
    )

    points = []
    for point, req_count in rows:
        points.append({
            'id': point.point_id,
            'name': point.location,
            'address': point.map_url,
            'hours': '',
            'contact': '',
            'status': 'active' if point.isActive else 'inactive',
            'requests_count': req_count
        })
    return render_template('company-portal/collection-points-admin.html', points=points)

@company_bp.route('/company/collection-points/add', methods=['GET', 'POST'])
def add_collection_point():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    error = None
    if request.method == 'POST':
        location = (request.form.get('name') or '').strip()
        map_url = (request.form.get('address') or '').strip()

        if not location: error = 'Point name is required.'
        elif not map_url: error = 'Address / map URL is required.'
        elif not is_valid_url(map_url): error = 'Address must be a valid URL starting with http or https.'
        else:
            new_point = models.CollectionPoint(company_id=company.company_id, location=location, map_url=map_url, isActive=True)
            db.session.add(new_point)
            db.session.commit()
            flash('Collection point added successfully.', 'success')
            return redirect(url_for('company.collection_points'))
    return render_template('company-portal/add-collection-point.html', error=error)

@company_bp.route('/company/collection-points/edit/<int:point_id>', methods=['GET', 'POST'])
def edit_collection_point(point_id):
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company: return redirect(url_for('auth.company_login'))

    point_obj = models.CollectionPoint.query.filter_by(point_id=point_id, company_id=company.company_id).first_or_404()
    error = None
    point = {'id': point_obj.point_id, 'name': point_obj.location, 'address': point_obj.map_url, 'hours': '', 'contact': ''}

    if request.method == 'POST':
        location = (request.form.get('name') or '').strip()
        map_url = (request.form.get('address') or '').strip()
        if not location: error = 'Point name is required.'
        elif not map_url: error = 'Address / map URL is required.'
        elif not is_valid_url(map_url): error = 'Address must be a valid URL starting with http or https.'
        else:
            point_obj.location = location
            point_obj.map_url = map_url
            db.session.commit()
            flash('Collection point updated successfully.', 'success')
            return redirect(url_for('company.collection_points'))
        point['name'] = location
        point['address'] = map_url
    return render_template('company-portal/edit-collection-point.html', point=point, error=error)

@company_bp.route('/company/collection-points/toggle/<int:point_id>', methods=['POST'])
def toggle_collection_point(point_id):
    if 'user_id' not in session or session.get('role') != 'company': return redirect(url_for('auth.company_login'))
    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company: return redirect(url_for('auth.company_login'))

    point = models.CollectionPoint.query.filter_by(point_id=point_id, company_id=company.company_id).first_or_404()
    requests_count = models.Request.query.filter_by(point_id=point.point_id).count()
    if point.isActive and requests_count > 0:
        flash('Cannot deactivate this point because it has active requests.', 'error')
        return redirect(url_for('company.collection_points'))
    point.isActive = not point.isActive
    db.session.commit()
    flash('Collection point status updated.', 'success')
    return redirect(url_for('company.collection_points'))

@company_bp.route('/company/collection-points/delete/<int:point_id>', methods=['POST'])
def delete_collection_point(point_id):
    if 'user_id' not in session or session.get('role') != 'company': return redirect(url_for('auth.company_login'))
    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company: return redirect(url_for('auth.company_login'))

    point = models.CollectionPoint.query.filter_by(point_id=point_id, company_id=company.company_id).first_or_404()
    requests_count = models.Request.query.filter_by(point_id=point.point_id).count()
    if requests_count > 0:
        flash('Cannot delete this point because it has requests linked to it.', 'error')
        return redirect(url_for('company.collection_points'))
    db.session.delete(point)
    db.session.commit()
    flash('Collection point deleted.', 'success')
    return redirect(url_for('company.collection_points'))

@company_bp.route('/company/statistics')
def statistics():
    if 'user_id' not in session or session.get('role') != 'company': return redirect(url_for('auth.company_login'))
    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company: return redirect(url_for('auth.company_login'))

    total_requests = models.Request.query.filter_by(company_id=company.company_id).count()
    total_devices = db.session.query(func.sum(models.Device.quantity)).join(models.Request).filter(models.Request.company_id == company.company_id).scalar() or 0
    devices_recycled = db.session.query(func.sum(models.Device.quantity)).join(models.Request).filter(models.Request.company_id == company.company_id, models.Request.status == 'Recycled').scalar() or 0
    completed_orders = models.Request.query.filter_by(company_id=company.company_id, status='Recycled').count()
    pending_orders = models.Request.query.filter_by(company_id=company.company_id, status='Received').count()

    status_raw = db.session.query(models.Request.status, func.count(models.Request.request_id)).filter(models.Request.company_id == company.company_id).group_by(models.Request.status).all()
    all_statuses = ["Received", "Under Recycling", "Recycled"]
    status_dict = {status: count for status, count in status_raw}
    labels = all_statuses
    data = [status_dict.get(s, 0) for s in all_statuses]

    device_type_raw = db.session.query(models.Device.type, func.sum(models.Device.quantity)).join(models.Request).filter(models.Request.company_id == company.company_id, models.Request.status == 'Recycled').group_by(models.Device.type).all()
    device_type_labels = [row[0] for row in device_type_raw]
    device_type_data = [int(row[1]) for row in device_type_raw]

    return render_template(
        'company-portal/statistics.html',
        total_requests=total_requests,
        total_devices=total_devices,
        devices_recycled=devices_recycled,
        completed_orders=completed_orders,
        pending_orders=pending_orders,
        labels=labels,
        data=data,
        device_type_labels=device_type_labels,
        device_type_data=device_type_data
    )

@company_bp.route('/company/reset-data', methods=['POST'])
def reset_data():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))
    
    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company:
        return redirect(url_for('auth.company_login'))

    try:
        # 1. Get all request IDs for this company
        requests = models.Request.query.filter_by(company_id=company.company_id).all()
        request_ids = [r.request_id for r in requests]

        if request_ids:
            # 2. Delete Request History associated with these requests
            models.RequestHistory.query.filter(models.RequestHistory.request_id.in_(request_ids)).delete(synchronize_session=False)
            
            # 3. Delete Devices associated with these requests
            models.Device.query.filter(models.Device.request_id.in_(request_ids)).delete(synchronize_session=False)
            
            # 4. Delete the Requests themselves
            models.Request.query.filter(models.Request.request_id.in_(request_ids)).delete(synchronize_session=False)
            
            db.session.commit()
            
        flash('All test data and requests have been successfully cleared.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting data: {str(e)}', 'error')
        
    return redirect(url_for('company.company_home'))
