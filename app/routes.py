from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')  # Serves an HTML page

@main.route('/api', methods=['GET'])
def api():
    return jsonify({"message": "Hello, Flask!"})  # Example API endpoint
