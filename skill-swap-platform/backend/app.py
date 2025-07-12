from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///skillswap.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, origins=["http://localhost:3000"])

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, default='')
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('Skill', backref='owner', lazy=True, cascade='all, delete-orphan')
    requests_sent = db.relationship('Request', foreign_keys='Request.requester_id', backref='requester', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    category = db.Column(db.String(50), default='other')
    level = db.Column(db.String(20), default='beginner')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('Request', backref='skill', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'level': self.level,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'skill_id': self.skill_id,
            'requester_id': self.requester_id,
            'message': self.message,
            'status': self.status,
            'skill': self.skill.to_dict() if self.skill else None,
            'requester': self.requester.to_dict() if self.requester else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        bio = data.get('bio', '').strip()

        if not name or not email or not password:
            return jsonify({'error': 'Name, email, and password are required'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        new_user = User(name=name, email=email, bio=bio)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

# Profile Routes
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get profile'}), 500

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        user.name = data.get('name', user.name).strip()
        user.bio = data.get('bio', user.bio).strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

# Skill Routes
@app.route('/api/skills', methods=['GET'])
def get_skills():
    try:
        skills = Skill.query.all()
        return jsonify([skill.to_dict() for skill in skills]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get skills'}), 500

@app.route('/api/skills', methods=['POST'])
@jwt_required()
def create_skill():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
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
            'skill': new_skill.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create skill'}), 500

@app.route('/api/skills/my-skills', methods=['GET'])
@jwt_required()
def get_my_skills():
    try:
        user_id = get_jwt_identity()
        skills = Skill.query.filter_by(owner_id=user_id).all()
        return jsonify([skill.to_dict() for skill in skills]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get skills'}), 500

@app.route('/api/skills/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_skill(id):
    try:
        user_id = get_jwt_identity()
        skill = Skill.query.get(id)
        
        if not skill:
            return jsonify({'error': 'Skill not found'}), 404
        
        if skill.owner_id != user_id:
            return jsonify({'error': 'Unauthorized to delete this skill'}), 403
        
        db.session.delete(skill)
        db.session.commit()
        
        return jsonify({'message': 'Skill deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete skill'}), 500

# Request Routes
@app.route('/api/requests', methods=['POST'])
@jwt_required()
def create_request():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        skill_id = data.get('skillId')
        message = data.get('message', '').strip()
        
        if not skill_id:
            return jsonify({'error': 'Skill ID is required'}), 400
        
        skill = Skill.query.get(skill_id)
        if not skill:
            return jsonify({'error': 'Skill not found'}), 404
        
        if skill.owner_id == user_id:
            return jsonify({'error': 'Cannot request your own skill'}), 400
        
        # Check if request already exists
        existing_request = Request.query.filter_by(
            skill_id=skill_id,
            requester_id=user_id
        ).first()
        
        if existing_request:
            return jsonify({'error': 'Request already exists for this skill'}), 400
        
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
            'request': new_request.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create request'}), 500

@app.route('/api/requests/received', methods=['GET'])
@jwt_required()
def get_received_requests():
    try:
        user_id = get_jwt_identity()
        
        # Get all skills owned by the user
        skills = Skill.query.filter_by(owner_id=user_id).all()
        skill_ids = [skill.id for skill in skills]
        
        # Get requests for these skills
        requests = Request.query.filter(Request.skill_id.in_(skill_ids)).all()
        
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get requests'}), 500

@app.route('/api/requests/sent', methods=['GET'])
@jwt_required()
def get_sent_requests():
    try:
        user_id = get_jwt_identity()
        requests = Request.query.filter_by(requester_id=user_id).all()
        return jsonify([req.to_dict() for req in requests]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get requests'}), 500

@app.route('/api/requests/<int:id>', methods=['PUT'])
@jwt_required()
def update_request(id):
    try:
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
        request_obj.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Request updated successfully',
            'request': request_obj.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update request'}), 500

@app.route('/api/requests/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_request(id):
    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete request'}), 500

# Admin Routes
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def admin_get_users():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get users'}), 500

@app.route('/api/admin/skills', methods=['GET'])
@jwt_required()
def admin_get_skills():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        skills = Skill.query.all()
        return jsonify([s.to_dict() for s in skills]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get skills'}), 500

@app.route('/api/admin/requests', methods=['GET'])
@jwt_required()
def admin_get_requests():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        requests = Request.query.all()
        return jsonify([r.to_dict() for r in requests]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get requests'}), 500

@app.route('/api/admin/users/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(id):
    try:
        user_id = get_jwt_identity()
        admin = User.query.get(user_id)
        
        if not admin or admin.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.id == admin.id:
            return jsonify({'error': 'Cannot delete yourself'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user'}), 500

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'SkillSwap API is running'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)