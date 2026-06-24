from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from extensions import db
import models
from datetime import datetime, timedelta
from sqlalchemy import func
import io
from utils.helpers import rtl
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/company/reports')
def reports():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))
    return render_template('company-portal/reports.html')

@reports_bp.route('/company/reports/download', methods=['POST'])
def download_report():
    if 'user_id' not in session or session.get('role') != 'company':
        return redirect(url_for('auth.company_login'))

    company = models.Company.query.filter_by(email=session.get('email')).first()
    if not company: return redirect(url_for('auth.company_login'))

    period = request.form.get('period', 'monthly')
    today = datetime.now().date()

    if period == 'monthly': start_date = today - timedelta(days=30)
    elif period == 'quarterly': start_date = today - timedelta(days=90)
    elif period == 'annual': start_date = today - timedelta(days=365)
    else: start_date = None

    base_query = models.Request.query.filter(models.Request.company_id == company.company_id)
    if start_date: base_query = base_query.filter(models.Request.request_date >= start_date)

    total_requests = base_query.count()
    total_devices = db.session.query(func.sum(models.Device.quantity)).join(models.Request).filter(
        models.Request.request_id.in_(base_query.with_entities(models.Request.request_id))
    ).scalar() or 0
    recycled_devices = db.session.query(func.sum(models.Device.quantity)).join(models.Request).filter(
        models.Request.request_id.in_(base_query.with_entities(models.Request.request_id)),
        models.Request.status == 'Recycled'
    ).scalar() or 0

    status_raw = db.session.query(models.Request.status, func.count(models.Request.request_id)).filter(
        models.Request.request_id.in_(base_query.with_entities(models.Request.request_id))
    ).group_by(models.Request.status).all()
    status_dict = {status: count for status, count in status_raw}

    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elements = []
        styles = getSampleStyleSheet()

        # Add custom styles
        styles.add(ParagraphStyle(name='ReportTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#111827'), spaceAfter=6))
        styles.add(ParagraphStyle(name='MetaText', parent=styles['Normal'], fontSize=10.5, textColor=colors.HexColor('#6b7280'), leading=14, spaceAfter=2))
        styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#374151'), leading=15))
        styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#374151'), spaceAfter=8, spaceBefore=10))

        # Title
        elements.append(Paragraph(rtl('Company Performance Report'), styles['ReportTitle']))
        elements.append(Spacer(1, 19))
        
        # Meta Info
        elements.append(Paragraph(f'<b>{rtl("Company Name")}:</b> {rtl(company.name)}', styles['MetaText']))
        elements.append(Paragraph(f'<b>{rtl("Registration No")}:</b> {rtl(company.registration_no)}', styles['MetaText']))
        elements.append(Paragraph(f'<b>{rtl("Report Date")}:</b> {datetime.now().strftime("%Y-%m-%d")}', styles['MetaText']))
        elements.append(Spacer(1, 25))

        # Performance Summary Section
        elements.append(Paragraph(rtl('Performance Summary'), styles['SectionTitle']))
        elements.append(Spacer(1, 8))
        summary_data = [
            [rtl('Metric'), rtl('Value')],
            [rtl('Total Requests'), total_requests],
            [rtl('Total Devices'), total_devices],
            [rtl('Recycled Devices'), recycled_devices]
        ]
        summary_table = Table(summary_data, colWidths=[250, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#bdbec1")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#111827')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#acadb0')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        # Status Overview Section
        elements.append(Paragraph(rtl('Request Status Overview'), styles['SectionTitle']))
        elements.append(Spacer(1, 8))
        status_data = [
            [rtl('Status'), rtl('Count')],
            [rtl('Received'), status_dict.get('Received', 0)],
            [rtl('Under Recycling'), status_dict.get('Under Recycling', 0)],
            [rtl('Recycled'), status_dict.get('Recycled', 0)]
        ]
        status_table = Table(status_data, colWidths=[250, 200])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#bdbec1")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#111827')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#acadb0")),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(status_table)
        elements.append(Spacer(1, 35))

        # Footer
        elements.append(Table([['']], colWidths=[450], rowHeights=[1], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e5e7eb'))]))
        elements.append(Spacer(1, 15))
        elements.append(Paragraph(f'<b>{rtl("Authorized Signature")}</b>', styles['NormalText']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph('______________________________', styles['NormalText']))
        elements.append(Spacer(1, 25))
        elements.append(Paragraph(rtl('Generated by GreenTech E-Waste Management System.'), styles['NormalText']))
        elements.append(Paragraph(rtl('All data is accurate as of the report date.'), styles['NormalText']))

        # Build PDF
        doc.build(elements)
        
        # Get data from buffer and ensure it's not empty
        pdf_value = buffer.getvalue()
        buffer.close()
        
        if not pdf_value:
            raise ValueError("Generated PDF is empty")

        # Return file using a fresh BytesIO for safety
        return send_file(
            io.BytesIO(pdf_value),
            as_attachment=True,
            download_name=f"{company.name.replace(' ', '_')}_{period}_report.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"Error generating report: {e}")
        # In case of error, we can return a flash message or redirect
        # For now, let's return a simple response so the user knows something went wrong
        return f"Error generating report: {str(e)}", 500
