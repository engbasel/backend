from flask import Blueprint, jsonify
from utils.database import get_faqs

faqs_bp = Blueprint('faqs', __name__)

@faqs_bp.route('/', methods=['GET'])
def get_all_faqs():
    """Get all FAQs"""
    try:
        faqs = get_faqs()
        return jsonify({'faqs': faqs})
    except Exception as e:
        print(f'Get FAQs error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve FAQs',
                'status': 500
            }
        }), 500
