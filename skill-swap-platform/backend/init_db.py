from app import app, db, User, Skill, bcrypt
from datetime import datetime

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin_email = 'admin@skillswap.com'
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(
                name='Admin',
                email=admin_email,
                password_hash=password_hash,
                role='admin',
                bio='System Administrator'
            )
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
        
        for user_data in sample_users:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password_hash=password_hash,
                    bio=user_data['bio']
                )
                db.session.add(user)
                print(f"✅ User created: {user_data['email']} / {user_data['password']}")
        
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
        
        for skill_data in sample_skills:
            owner = User.query.filter_by(email=skill_data['owner_email']).first()
            if owner:
                existing_skill = Skill.query.filter_by(
                    name=skill_data['name'],
                    owner_id=owner.id
                ).first()
                
                if not existing_skill:
                    skill = Skill(
                        name=skill_data['name'],
                        description=skill_data['description'],
                        category=skill_data['category'],
                        level=skill_data['level'],
                        owner_id=owner.id
                    )
                    db.session.add(skill)
                    print(f"✅ Skill created: {skill_data['name']} by {owner.name}")
        
        # Commit all changes
        db.session.commit()
        print("\n🎉 Database initialized successfully!")
        print("\n📋 Sample Data Created:")
        print("- Admin user: admin@skillswap.com / admin123")
        print("- Sample users: john@example.com, jane@example.com, mike@example.com (password: password123)")
        print("- 6 sample skills across different categories")
        print("\n🚀 You can now start the backend server with: python app.py")

if __name__ == '__main__':
    init_database() 