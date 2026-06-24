from flask import Blueprint, request, jsonify, session
from utils.ai_classifier import classify_device, get_recommendations

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ai/classify', methods=['POST'])
def classify():
    """
    Accepts JSON: {"device_name": "iPhone 13"}
    Returns JSON classification data.
    """
    data = request.get_json() or {}
    device_name = data.get('device_name', '')
    
    result = classify_device(device_name)
    return jsonify(result)

@ai_bp.route('/api/ai/recommend', methods=['POST'])
def recommend():
    """
    Accepts JSON: {"device_type": "Mobile", "condition": "Working"}
    Returns JSON list of recommendations.
    """
    data = request.get_json() or {}
    device_type = data.get('device_type', 'Other')
    condition = data.get('condition', 'Working')
    lang = session.get('lang', 'en')
    
    recommendations = get_recommendations(device_type, condition, lang)
    return jsonify({"recommendations": recommendations})
