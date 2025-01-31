import json

from flask import Response
from flask import Blueprint, request, jsonify
from werkzeug.routing import Rule

dynamic_api = Blueprint("dynamic_api", __name__)

# In-memory storage for dynamically created APIs
dynamic_routes = {}

def add_dynamic_route(app, endpoint, method, response_body):
    """
    Dynamically add a route to the Flask app.
    """
    # Define the view function
    def dynamic_view():
        response_json = json.dumps(response_body, indent=2, sort_keys=False)
        return Response(response_json, content_type="application/json")

    # Add the rule to Flask's URL map
    rule = Rule(endpoint, methods=[method], endpoint=endpoint)
    app.url_map.add(rule)

    # Map the endpoint to the view function
    app.view_functions[endpoint] = dynamic_view

@dynamic_api.route('/generate_api', methods=['POST'])
def handle_generate_api():
    """
    API to dynamically generate new routes.
    """
    from flask import current_app

    # Access the current app instance from Flask's application context
    app = current_app

    data = request.get_json()

    endpoint = data.get("endpoint")
    method = data.get("method", "GET")
    response_body = data.get("response_body", {})

    if not endpoint:
        return jsonify({"error": "Endpoint is required"}), 400

    # Check if the endpoint already exists
    if endpoint in dynamic_routes:
        return jsonify({"error": "Endpoint already exists"}), 400

    # Add the dynamic route
    add_dynamic_route(app, endpoint, method, response_body)
    dynamic_routes[endpoint] = {"method": method, "response_body": response_body}

    return jsonify({"message": "API created successfully!", "endpoint": endpoint})

@dynamic_api.route('/list_apis', methods=['GET'])
def list_apis():
    """
    List all dynamically created APIs.
    """
    return jsonify({"dynamic_routes": dynamic_routes})