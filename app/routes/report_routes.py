"""Makes all user reports."""
import os
import json
from flask import Blueprint, abort, jsonify, request, send_file, Response, render_template
from app.controllers import OrderController
from app.controllers.user_controller import UserController
from app.controllers.report_controller import ReportController

from app.config import Stripe
blueprint_report = Blueprint('report', __name__)


@blueprint_report.route('/get_report_days')
def days_report():
    """Makes all user reports."""
    ReportController.test_report()
    return send_file('templates\days_report.csv',
                     mimetype='text/csv',
                     attachment_filename='days_report.csv',
                     as_attachment=True)
@blueprint_report.route('/get_report_weeks')
def weeks_report():
    """Makes all user reports."""
    ReportController.test_report()
    return send_file('templates\weeks_report.csv',
                     mimetype='text/csv',
                     attachment_filename='weeks_report.csv',
                     as_attachment=True)

@blueprint_report.route('/get_report_months')
def months_report():
    """Makes all user reports."""
    ReportController.test_report()
    return send_file('templates\months_report.csv',
                     mimetype='text/csv',
                     attachment_filename='months_report.csv',
                     as_attachment=True)

@blueprint_report.route('/get_report_years')
def years_report():
    """Makes all user reports."""
    ReportController.test_report()
    return send_file('templates\years_report.csv',
                     mimetype='text/csv',
                     attachment_filename='years_report.csv',
                     as_attachment=True)

@blueprint_report.route('/show_report')
def show_report():
    """Makes all user reports."""
    return render_template('reports.html')