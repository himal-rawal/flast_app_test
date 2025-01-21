from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

pastebin_api = Blueprint('pastebin_api', __name__, url_prefix='/api/pastebin')

# Create a new paste (text/code)
@pastebin_api.route('/create', methods=['POST'])
def create_snippet():
    # Import db and model inside the function to avoid circular imports
    from app import db
    from app.models import PasteText

    data = request.json

    if not data or 'content' not in data or not data['content'].strip():
        return jsonify({"error": "Content is required"}), 400

    is_protected = data.get('is_protected', False)
    password = None

    if is_protected:
        if 'password' not in data or not data['password'].strip():
            return jsonify({"error": "Password is required for protected snippets"}), 400
        password = generate_password_hash(data['password'])

    snippet = PasteText(
        content=data['content'],
        language=data.get('language'),
        is_protected=is_protected,
        password=password
    )

    db.session.add(snippet)
    db.session.commit()

    return jsonify({"message": "Snippet created successfully", "id": snippet.id}), 201

# Retrieve a paste by ID
@pastebin_api.route('/<int:snippet_id>', methods=['GET'])
def get_snippet(snippet_id):
    # Import db and model inside the function to avoid circular imports
    from app import db
    from app.models import PasteText

    snippet = PasteText.query.get(snippet_id)
    if not snippet:
        return jsonify({"error": "Snippet not found"}), 404

    if snippet.is_protected:
        password = request.args.get('password')
        if not password or not check_password_hash(snippet.password, password):
            return jsonify({"error": "Invalid or missing password"}), 403

    return jsonify({
        "id": snippet.id,
        "content": snippet.content,
        "language": snippet.language,
        "is_protected": snippet.is_protected,
        "created_at": snippet.created_at
    }), 200


@pastebin_api.route('/all', methods=['GET'])
def get_all_snippets():
    """
    Get all pasted texts in paginated form, sorted by latest first.
    Query parameters:
      - page: Page number (default: 1)
      - per_page: Number of items per page (default: 20)
    """
    from app import db
    from app.models import PasteText
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Query the database for snippets, ordered by latest first
    snippets = PasteText.query.order_by(PasteText.created_at.desc()).paginate(page=page, per_page=per_page)

    # Prepare the response data
    data = {
        "page": snippets.page,
        "per_page": snippets.per_page,
        "total": snippets.total,
        "pages": snippets.pages,
        "items": [
            {
                "id": snippet.id,
                "content": snippet.content,
                "language": snippet.language,
                "is_protected": snippet.is_protected,
                "created_at": snippet.created_at
            }
            for snippet in snippets.items
        ]
    }

    return jsonify(data), 200

