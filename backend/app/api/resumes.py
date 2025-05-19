from flask import Blueprint, request, jsonify
from app.db.mongodb import get_db
from app.core.security import hash_password
from bson.objectid import ObjectId

resumes_bp = Blueprint('resumes', __name__)

@resumes_bp.route('/resumes', methods=['POST'])
def upload_resume():
    data = request.json
    if not data or 'user_id' not in data or 'resume_data' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    db = get_db()
    resume = {
        'user_id': data['user_id'],
        'resume_data': data['resume_data'],
        'uploaded_at': datetime.utcnow()
    }
    result = db.resumes.insert_one(resume)
    return jsonify({'id': str(result.inserted_id)}), 201

@resumes_bp.route('/resumes/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    db = get_db()
    resume = db.resumes.find_one({'_id': ObjectId(resume_id)})
    if resume is None:
        return jsonify({'error': 'Resume not found'}), 404
    return jsonify({'id': str(resume['_id']), 'user_id': resume['user_id'], 'resume_data': resume['resume_data']}), 200

@resumes_bp.route('/resumes/user/<user_id>', methods=['GET'])
def get_user_resumes(user_id):
    db = get_db()
    resumes = list(db.resumes.find({'user_id': user_id}))
    return jsonify([{'id': str(resume['_id']), 'resume_data': resume['resume_data']} for resume in resumes]), 200