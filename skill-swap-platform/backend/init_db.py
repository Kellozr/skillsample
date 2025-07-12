from app import app, db, User, Skill, Request
from datetime import datetime

def init_database():
    with app.app_context():
        # Drop all tables and recreate them
        print("🔄 Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("🔧 Creating database tables...")
        db.create_all()
        
        # Create admin user
        admin_email = 'admin@skillswap.com'
        admin = User(
            name='Admin',
            email=admin_email,
            role='admin',
            bio='System Administrator'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ Admin user created: admin@skillswap.com / admin123")
        
        # Create sample users
        sample_users = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'password': 'password123',
                'bio': 'Web developer with 5 years of experience'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'password': 'password123',
                'bio': 'UI/UX designer passionate about creating beautiful interfaces'
            },
            {
                'name': 'Mike Johnson',
                'email': 'mike@example.com',
                'password': 'password123',
                'bio': 'Guitar teacher with 10 years of experience'
            }
        ]
        
        users = {}
        for user_data in sample_users:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                bio=user_data['bio']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            users[user_data['email']] = user
            print(f"✅ User created: {user_data['email']} / {user_data['password']}")
        
        # Commit users first
        db.session.commit()
        
        # Create sample skills
        sample_skills = [
            {
                'name': 'React Development',
                'description': 'Learn React.js from basics to advanced concepts including hooks, context, and state management.',
                'category': 'programming',
                'level': 'intermediate',
                'owner_email': 'john@example.com'
            },
            {
                'name': 'UI/UX Design',
                'description': 'Master the principles of user interface and user experience design using Figma and other tools.',
                'category': 'design',
                'level': 'advanced',
                'owner_email': 'jane@example.com'
            },
            {
                'name': 'Guitar Lessons',
                'description': 'Learn acoustic and electric guitar from basic chords to advanced techniques and music theory.',
                'category': 'music',
                'level': 'expert',
                'owner_email': 'mike@example.com'
            },
            {
                'name': 'Python Programming',
                'description': 'Learn Python programming from fundamentals to web development with Django and Flask.',
                'category': 'programming',
                'level': 'beginner',
                'owner_email': 'john@example.com'
            },
            {
                'name': 'Digital Marketing',
                'description': 'Learn digital marketing strategies including SEO, social media marketing, and content creation.',
                'category': 'marketing',
                'level': 'intermediate',
                'owner_email': 'jane@example.com'
            },
            {
                'name': 'Spanish Language',
                'description': 'Learn Spanish from basic conversation to advanced grammar and cultural understanding.',
                'category': 'languages',
                'level': 'beginner',
                'owner_email': 'mike@example.com'
            }
        ]
        
        skills = {}
        for skill_data in sample_skills:
            owner = User.query.filter_by(email=skill_data['owner_email']).first()
            if owner:
                skill = Skill(
                    name=skill_data['name'],
                    description=skill_data['description'],
                    category=skill_data['category'],
                    level=skill_data['level'],
                    owner_id=owner.id
                )
                db.session.add(skill)
                skills[skill_data['name']] = skill
                print(f"✅ Skill created: {skill_data['name']} by {owner.name}")
        
        # Commit skills
        db.session.commit()
        
        # Create sample requests
        sample_requests = [
            {
                'skill_name': 'React Development',
                'requester_email': 'jane@example.com',
                'message': 'I would love to learn React to improve my frontend skills!',
                'status': 'pending'
            },
            {
                'skill_name': 'UI/UX Design',
                'requester_email': 'mike@example.com',
                'message': 'I want to learn design principles for my music website.',
                'status': 'accepted'
            },
            {
                'skill_name': 'Guitar Lessons',
                'requester_email': 'john@example.com',
                'message': 'I have always wanted to learn guitar. Can you help?',
                'status': 'pending'
            }
        ]
        
        for request_data in sample_requests:
            skill = Skill.query.filter_by(name=request_data['skill_name']).first()
            requester = User.query.filter_by(email=request_data['requester_email']).first()
            
            if skill and requester and skill.owner_id != requester.id:
                request_obj = Request(
                    skill_id=skill.id,
                    requester_id=requester.id,
                    message=request_data['message'],
                    status=request_data['status']
                )
                db.session.add(request_obj)
                print(f"✅ Request created: {requester.name} -> {skill.name}")
        
        # Final commit
        db.session.commit()
        print("\n🎉 Database initialized successfully!")
        print("\n📋 Sample Data Created:")
        print("- Admin user: admin@skillswap.com / admin123")
        print("- Sample users: john@example.com, jane@example.com, mike@example.com (password: password123)")
        print("- 6 sample skills across different categories")
        print("- 3 sample requests")
        print("\n🚀 You can now start the backend server with: python app.py")

if __name__ == '__main__':
    init_database()