from flask import Blueprint, request, jsonify
from app.db.mongodb import get_resume_by_id, verify_resume
from app.core.security import verify_signature

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/verify/<resume_id>', methods=['POST'])
def verify(resume_id):
    data = request.json
    signature = data.get('signature')
    
    resume = get_resume_by_id(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    is_verified = verify_signature(resume['data'], signature)
    if is_verified:
        return jsonify({'message': 'Resume is verified'}), 200
    else:
        return jsonify({'message': 'Resume verification failed'}), 400