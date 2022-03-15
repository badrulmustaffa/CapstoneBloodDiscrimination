from flask import Flask, render_template, request, Blueprint
from flask_login import login_required, current_user



machine_learning_algorithm_bp = Blueprint('machine_learning_algorithm_bp', __name__, url_prefix='/machine_learning_algorithm')

@machine_learning_algorithm_bp.route('/')
@login_required
def index_view():
    return render_template('index.html')


@machine_learning_algorithm_bp.route('/predict/',methods=['GET','POST'])
def predict():
    response = "For ML Prediction"
    return response
