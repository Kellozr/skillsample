from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging
from functools import wraps

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced error handling decorator
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occurred'}), 500
    return decorated_function

# Database Models with enhanced relationships
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, default='')
    role = db.Column(db.String(20), default='user')
    avatar_url = db.Column(db.String(255), default='')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Enhanced relationships
    skills = db.relationship('Skill', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    requests_sent = db.relationship('Request', foreign_keys='Request.requester_id', 
                                  backref='requester', lazy='dynamic', cascade='all, delete-orphan')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id',
                                  backref='reviewer', lazy='dynamic', cascade='all, delete-orphan')
    reviews_received = db.relationship('Review', foreign_keys='Review.reviewee_id',
                                     backref='reviewee', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_stats=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'role': self.role,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_stats:
            data.update({
                'skills_count': self.skills.count(),
                'requests_sent_count': self.requests_sent.count(),
                'average_rating': self.get_average_rating()
            })
        
        return data

    def get_average_rating(self):
        reviews = self.reviews_received.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, default='')
    category = db.Column(db.String(50), default='other', index=True)
    level = db.Column(db.String(20), default='beginner', index=True)
    tags = db.Column(db.Text, default='')  # JSON string of tags
    duration_estimate = db.Column(db.String(50), default='')  # e.g., "2-4 weeks"
    prerequisites = db.Column(db.Text, default='')
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('Request', backref='skill', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='skill', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_stats=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'level': self.level,
            'tags': self.tags,
            'duration_estimate': self.duration_estimate,
            'prerequisites': self.prerequisites,
            'is_active': self.is_active,
            'view_count': self.view_count,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stats:
            data.update({
                'requests_count': self.requests.count(),
                'average_rating': self.get_average_rating(),
                'reviews_count': self.reviews.count()
            })
        
        return data

    def get_average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    message = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending', index=True)  # pending, accepted, rejected, completed
    priority = db.Column(db.String(10), default='normal')  # low, normal, high
    preferred_schedule = db.Column(db.Text, default='')
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'skill_id': self.skill_id,
            'requester_id': self.requester_id,
            'message': self.message,
            'status': self.status,
            'priority': self.priority,
            'preferred_schedule': self.preferred_schedule,
            'notes': self.notes,
            'skill': self.skill.to_dict() if self.skill else None,
            'requester': self.requester.to_dict() if self.requester else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, default='')
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'skill_id': self.skill_id,
            'reviewer_id': self.reviewer_id,
            'reviewee_id': self.reviewee_id,
            'rating': self.rating,
            'comment': self.comment,
            'is_public': self.is_public,
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'skill': self.skill.to_dict() if self.skill else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Enhanced Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
@handle_errors
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    bio = data.get('bio', '').strip()

    # Enhanced validation
    if not name or len(name) < 2:
        return jsonify({'error': 'Name must be at least 2 characters long'}), 400
    
    if not email or '@' not in email:
        return jsonify({'error': 'Valid email is required'}), 400

    if not password or len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(name=name, email=email, bio=bio)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    logger.info(f"New user registered: {email}")
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': new_user.to_dict()
    }), 201

@app.route('/api/auth/login', methods=['POST'])
@handle_errors
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401

    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    logger.info(f"User logged in: {email}")
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

# Enhanced Profile Routes
@app.route('/api/profile', methods=['GET'])
@jwt_required()
@handle_errors
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict(include_stats=True)), 200

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
@handle_errors
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        name = data['name'].strip()
        if len(name) >= 2:
            user.name = name
        else:
            return jsonify({'error': 'Name must be at least 2 characters long'}), 400
    
    if 'bio' in data:
        user.bio = data['bio'].strip()
    
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url'].strip()
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200

# Enhanced Skill Routes
@app.route('/api/skills', methods=['GET'])
@handle_errors
def get_skills():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    level = request.args.get('level')
    search = request.args.get('search')
    
    query = Skill.query.filter_by(is_active=True)
    
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if level and level != 'all':
        query = query.filter_by(level=level)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Skill.name.ilike(search_term),
                Skill.description.ilike(search_term),
                Skill.tags.ilike(search_term)
            )
        )
    
    skills = query.order_by(Skill.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'skills': [skill.to_dict(include_stats=True) for skill in skills.items],
        'total': skills.total,
        'pages': skills.pages,
        'current_page': page
    }), 200

@app.route('/api/skills', methods=['POST'])
@jwt_required()
@handle_errors
def create_skill():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    category = data.get('category', 'other')
    level = data.get('level', 'beginner')
    tags = data.get('tags', '')
    duration_estimate = data.get('duration_estimate', '').strip()
    prerequisites = data.get('prerequisites', '').strip()
    
    if not name or len(name) < 3:
        return jsonify({'error': 'Skill name must be at least 3 characters long'}), 400
    
    if not description or len(description) < 10:
        return jsonify({'error': 'Description must be at least 10 characters long'}), 400
    
    new_skill = Skill(
        name=name,
        description=description,
        category=category,
        level=level,
        tags=tags,
        duration_estimate=duration_estimate,
        prerequisites=prerequisites,
        owner_id=user_id
    )
    
    db.session.add(new_skill)
    db.session.commit()
    
    logger.info(f"New skill created: {name} by user {user_id}")
    
    return jsonify({
        'message': 'Skill created successfully',
        'skill': new_skill.to_dict()
    }), 201

@app.route('/api/skills/my-skills', methods=['GET'])
@jwt_required()
@handle_errors
def get_my_skills():
    user_id = get_jwt_identity()
    skills = Skill.query.filter_by(owner_id=user_id).order_by(Skill.created_at.desc()).all()
    return jsonify([skill.to_dict(include_stats=True) for skill in skills]), 200

@app.route('/api/skills/<int:id>', methods=['GET'])
@handle_errors
def get_skill(id):
    skill = Skill.query.get(id)
    if not skill or not skill.is_active:
        return jsonify({'error': 'Skill not found'}), 404
    
    # Increment view count
    skill.view_count += 1
    db.session.commit()
    
    return jsonify(skill.to_dict(include_stats=True)), 200

@app.route('/api/skills/<int:id>', methods=['PUT'])
@jwt_required()
@handle_errors
def update_skill(id):
    user_id = get_jwt_identity()
    skill = Skill.query.get(id)
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    if skill.owner_id != user_id:
        return jsonify({'error': 'Unauthorized to update this skill'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    for field in ['name', 'description', 'category', 'level', 'tags', 'duration_estimate', 'prerequisites']:
        if field in data:
            setattr(skill, field, data[field])
    
    skill.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Skill updated successfully',
        'skill': skill.to_dict()
    }), 200

@app.route('/api/skills/<int:id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_skill(id):
    user_id = get_jwt_identity()
    skill = Skill.query.get(id)
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    if skill.owner_id != user_id:
        return jsonify({'error': 'Unauthorized to delete this skill'}), 403
    
    db.session.delete(skill)
    db.session.commit()
    
    logger.info(f"Skill deleted: {skill.name} by user {user_id}")
    
    return jsonify({'message': 'Skill deleted successfully'}), 200

# Enhanced Request Routes
@app.route('/api/requests', methods=['POST'])
@jwt_required()
@handle_errors
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    skill_id = data.get('skillId')
    message = data.get('message', '').strip()
    priority = data.get('priority', 'normal')
    preferred_schedule = data.get('preferred_schedule', '').strip()
    
    if not skill_id:
        return jsonify({'error': 'Skill ID is required'}), 400
    
    skill = Skill.query.get(skill_id)
    if not skill or not skill.is_active:
        return jsonify({'error': 'Skill not found'}), 404
    
    if skill.owner_id == user_id:
        return jsonify({'error': 'Cannot request your own skill'}), 400
    
    # Check if request already exists
    existing_request = Request.query.filter_by(
        skill_id=skill_id,
        requester_id=user_id,
        status='pending'
    ).first()
    
    if existing_request:
        return jsonify({'error': 'You already have a pending request for this skill'}), 400
    
    new_request = Request(
        skill_id=skill_id,
        requester_id=user_id,
        message=message,
        priority=priority,
        preferred_schedule=preferred_schedule,
        status='pending'
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    logger.info(f"New request created: skill {skill_id} by user {user_id}")
    
    return jsonify({
        'message': 'Request created successfully',
        'request': new_request.to_dict()
    }), 201

@app.route('/api/requests/received', methods=['GET'])
@jwt_required()
@handle_errors
def get_received_requests():
    user_id = get_jwt_identity()
    
    # Get all skills owned by the user
    skills = Skill.query.filter_by(owner_id=user_id).all()
    skill_ids = [skill.id for skill in skills]
    
    # Get requests for these skills
    requests = Request.query.filter(Request.skill_id.in_(skill_ids)).order_by(
        Request.created_at.desc()
    ).all()
    
    return jsonify([req.to_dict() for req in requests]), 200

@app.route('/api/requests/sent', methods=['GET'])
@jwt_required()
@handle_errors
def get_sent_requests():
    user_id = get_jwt_identity()
    requests = Request.query.filter_by(requester_id=user_id).order_by(
        Request.created_at.desc()
    ).all()
    return jsonify([req.to_dict() for req in requests]), 200

@app.route('/api/requests/<int:id>', methods=['PUT'])
@jwt_required()
@handle_errors
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
    notes = data.get('notes', '')
    
    if new_status not in ['accepted', 'rejected', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    
    request_obj.status = new_status
    request_obj.notes = notes
    request_obj.updated_at = datetime.utcnow()
    
    if new_status == 'completed':
        request_obj.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    logger.info(f"Request {id} updated to {new_status} by user {user_id}")
    
    return jsonify({
        'message': f'Request {new_status} successfully',
        'request': request_obj.to_dict()
    }), 200

@app.route('/api/requests/<int:id>', methods=['DELETE'])
@jwt_required()
@handle_errors
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
    
    logger.info(f"Request {id} deleted by user {user_id}")
    
    return jsonify({'message': 'Request deleted successfully'}), 200

# Analytics and Stats Routes
@app.route('/api/stats/dashboard', methods=['GET'])
@jwt_required()
@handle_errors
def get_dashboard_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    stats = {
        'skills_offered': user.skills.filter_by(is_active=True).count(),
        'requests_received': Request.query.join(Skill).filter(
            Skill.owner_id == user_id
        ).count(),
        'requests_sent': user.requests_sent.count(),
        'completed_sessions': Request.query.filter_by(
            requester_id=user_id, status='completed'
        ).count(),
        'average_rating': user.get_average_rating(),
        'total_reviews': user.reviews_received.count()
    }
    
    return jsonify(stats), 200

# Admin Routes (Enhanced)
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
@handle_errors
def admin_get_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'users': [u.to_dict(include_stats=True) for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    }), 200

@app.route('/api/admin/skills', methods=['GET'])
@jwt_required()
@handle_errors
def admin_get_skills():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    skills = Skill.query.order_by(Skill.created_at.desc()).all()
    return jsonify([s.to_dict(include_stats=True) for s in skills]), 200

@app.route('/api/admin/requests', methods=['GET'])
@jwt_required()
@handle_errors
def admin_get_requests():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    requests = Request.query.order_by(Request.created_at.desc()).all()
    return jsonify([r.to_dict() for r in requests]), 200

@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
@handle_errors
def admin_get_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_skills': Skill.query.count(),
        'active_skills': Skill.query.filter_by(is_active=True).count(),
        'total_requests': Request.query.count(),
        'pending_requests': Request.query.filter_by(status='pending').count(),
        'completed_requests': Request.query.filter_by(status='completed').count(),
        'categories': db.session.query(
            Skill.category, db.func.count(Skill.id)
        ).group_by(Skill.category).all()
    }
    
    return jsonify(stats), 200

@app.route('/api/admin/users/<int:id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def admin_delete_user(id):
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
    
    logger.info(f"User {id} deleted by admin {user_id}")
    
    return jsonify({'message': 'User deleted successfully'}), 200

# Health and utility endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'SkillSwap API is running',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(
        Skill.category, 
        db.func.count(Skill.id).label('count')
    ).filter_by(is_active=True).group_by(Skill.category).all()
    
    return jsonify([
        {'name': cat[0], 'count': cat[1]} for cat in categories
    ]), 200

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    logger.info("Starting SkillSwap API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)