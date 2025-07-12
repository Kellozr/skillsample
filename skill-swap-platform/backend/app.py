from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skills = db.relationship('Skill', backref='owner', lazy=True)
    requests_sent = db.relationship('Request', foreign_keys='Request.requester_id', backref='requester', lazy=True)
    requests_received = db.relationship('Request', foreign_keys='Request.skill_id', backref='skill_owner', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    level = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    requests = db.relationship('Request', backref='skill', lazy=True)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# Helper function to serialize database objects
def serialize(obj):
    if isinstance(obj, db.Model):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    return obj

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    bio = data.get('bio', '')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(name=name, email=email, bio=bio)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': serialize(new_user)
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': serialize(user)
    }), 200

# Profile Routes
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(serialize(user)), 200

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': serialize(user)
    }), 200

# Skill Routes
@app.route('/api/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify([serialize(skill) for skill in skills]), 200

@app.route('/api/skills', methods=['POST'])
@jwt_required()
def create_skill():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    category = data.get('category', 'other')
    level = data.get('level', 'beginner')
    
    if not name:
        return jsonify({'error': 'Skill name is required'}), 400
    
    new_skill = Skill(
        name=name,
        description=description,
        category=category,
        level=level,
        owner_id=user_id
    )
    
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({
        'message': 'Skill created successfully',
        'skill': serialize(new_skill)
    }), 201

@app.route('/api/skills/my-skills', methods=['GET'])
@jwt_required()
def get_my_skills():
    user_id = get_jwt_identity()
    skills = Skill.query.filter_by(owner_id=user_id).all()
    return jsonify([serialize(skill) for skill in skills]), 200

@app.route('/api/skills/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_skill(id):
    user_id = get_jwt_identity()
    skill = Skill.query.get(id)
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    if skill.owner_id != user_id:
        return jsonify({'error': 'Unauthorized to delete this skill'}), 403
    
    db.session.delete(skill)
    db.session.commit()
    
    return jsonify({'message': 'Skill deleted successfully'}), 200

# Request Routes
@app.route('/api/requests', methods=['POST'])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    skill_id = data.get('skillId')
    message = data.get('message', '')
    
    if not skill_id:
        return jsonify({'error': 'Skill ID is required'}), 400
    
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    if skill.owner_id == user_id:
        return jsonify({'error': 'Cannot request your own skill'}), 400
    
    new_request = Request(
        skill_id=skill_id,
        requester_id=user_id,
        message=message,
        status='pending'
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Request created successfully',
        'request': serialize(new_request)
    }), 201

@app.route('/api/requests/received', methods=['GET'])
@jwt_required()
def get_received_requests():
    user_id = get_jwt_identity()
    
    # Get all skills owned by the user
    skills = Skill.query.filter_by(owner_id=user_id).all()
    skill_ids = [skill.id for skill in skills]
    
    # Get requests for these skills
    requests = Request.query.filter(Request.skill_id.in_(skill_ids)).all()
    
    return jsonify([serialize(req) for req in requests]), 200

@app.route('/api/requests/sent', methods=['GET'])
@jwt_required()
def get_sent_requests():
    user_id = get_jwt_identity()
    requests = Request.query.filter_by(requester_id=user_id).all()
    return jsonify([serialize(req) for req in requests]), 200

@app.route('/api/requests/<int:id>', methods=['PUT'])
@jwt_required()
def update_request(id):
    user_id = get_jwt_identity()
    request_obj = Request.query.get(id)
    
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404
    
    # Check if user is the owner of the skill
    if request_obj.skill.owner_id != user_id:
        return jsonify({'error': 'Unauthorized to update this request'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['accepted', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    request_obj.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': 'Request updated successfully',
        'request': serialize(request_obj)
    }), 200

@app.route('/api/requests/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_request(id):
    user_id = get_jwt_identity()
    request_obj = Request.query.get(id)
    
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404
    
    # Only requester can delete their own request
    if request_obj.requester_id != user_id:
        return jsonify({'error': 'Unauthorized to delete this request'}), 403
    
    db.session.delete(request_obj)
    db.session.commit()
    
    return jsonify({'message': 'Request deleted successfully'}), 200

# Admin Routes
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def admin_get_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([serialize(u) for u in users]), 200

@app.route('/api/admin/skills', methods=['GET'])
@jwt_required()
def admin_get_skills():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    skills = Skill.query.all()
    return jsonify([serialize(s) for s in skills]), 200

@app.route('/api/admin/requests', methods=['GET'])
@jwt_required()
def admin_get_requests():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    requests = Request.query.all()
    return jsonify([serialize(r) for r in requests]), 200

@app.route('/api/admin/users/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(id):
    user_id = get_jwt_identity()
    admin = User.query.get(user_id)
    
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True) 