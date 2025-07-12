import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1>Welcome to SkillSwap</h1>
          <p className="hero-subtitle">
            Connect with people who can teach you new skills and share your expertise with others.
            Learn, grow, and build meaningful connections through skill exchange.
          </p>
          
          {!user ? (
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary">
                Get Started
              </Link>
              <Link to="/login" className="btn btn-secondary">
                Sign In
              </Link>
            </div>
          ) : (
            <div className="hero-actions">
              <Link to="/browse" className="btn btn-primary">
                Browse Skills
              </Link>
              <Link to="/profile" className="btn btn-secondary">
                My Profile
              </Link>
            </div>
          )}
        </div>
      </div>

      <div className="features-section">
        <h2>How It Works</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Find Skills</h3>
            <p>Browse through a wide variety of skills offered by our community members. From programming to cooking, there's something for everyone.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🤝</div>
            <h3>Make Requests</h3>
            <p>Send requests to learn from people who have the skills you want to acquire. Connect with mentors and start your learning journey.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3>Share Knowledge</h3>
            <p>Offer your own skills to help others learn. Teaching is a great way to reinforce your knowledge and make new connections.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🌟</div>
            <h3>Build Community</h3>
            <p>Join a community of learners and teachers. Build lasting relationships while developing new skills together.</p>
          </div>
        </div>
      </div>

      <div className="categories-section">
        <h2>Popular Skill Categories</h2>
        <div className="categories-grid">
          <div className="category-card">
            <h3>Programming</h3>
            <p>Web development, mobile apps, data science, and more</p>
          </div>
          <div className="category-card">
            <h3>Design</h3>
            <p>Graphic design, UI/UX, web design, and creative skills</p>
          </div>
          <div className="category-card">
            <h3>Languages</h3>
            <p>Learn new languages and improve your communication skills</p>
          </div>
          <div className="category-card">
            <h3>Music</h3>
            <p>Instruments, music theory, production, and performance</p>
          </div>
          <div className="category-card">
            <h3>Cooking</h3>
            <p>Culinary arts, baking, international cuisine, and techniques</p>
          </div>
          <div className="category-card">
            <h3>Marketing</h3>
            <p>Digital marketing, social media, SEO, and business skills</p>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <h2>Ready to Start Learning?</h2>
        <p>Join thousands of people who are already sharing and learning skills on SkillSwap.</p>
        {!user ? (
          <Link to="/register" className="btn btn-primary btn-large">
            Join SkillSwap Today
          </Link>
        ) : (
          <Link to="/browse" className="btn btn-primary btn-large">
            Explore Skills
          </Link>
        )}
      </div>
    </div>
  );
};

export default HomePage; 