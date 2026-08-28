from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/sobre')
def about():
    return render_template('about.html')

@main_bp.route('/hidrogenio-verde')
def hydrogen():
    return render_template('hydrogen.html')