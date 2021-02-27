"""Makes all user reports."""
import os
import json
from flask import Blueprint, abort, jsonify, request, send_file, Response
from app.controllers import OrderController
from app.controllers.user_controller import UserController
from app.controllers.report_controller import ReportController

from app.config import Stripe
blueprint_report = Blueprint('report', __name__)


@blueprint_report.route('/get_report')
def test_report():
    """Makes all user reports."""
    ReportController.test_report()
    return send_file('..\days_report.csv',
                     mimetype='text/csv',
                     attachment_filename='days_report.csv',
                     as_attachment=True)
