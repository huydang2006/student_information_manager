# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.services.home_service import HomeService
from app.models.program_model import Program
from app.models.home import DashboardService
import plotly.express as px
import plotly.io as pio

home_bp = Blueprint('home', __name__, url_prefix='/home', template_folder='../templates')

@home_bp.route("/")
def describe():
    summary = DashboardService.get_tuition_summary()

    labels = [row["payment_status"] for row in summary]
    values = [row["total_count"] for row in summary]

    fig = px.pie(values=values, names=labels, title="Tuition Fee Summary")

    # Xuất HTML của biểu đồ
    chart_html = pio.to_html(fig)

    return render_template("home.html", chart_html=chart_html)