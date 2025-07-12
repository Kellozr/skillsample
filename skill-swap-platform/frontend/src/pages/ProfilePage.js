import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user, api } = useAuth();
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [newSkill, setNewSkill] = useState({
    name: '',
    description: '',
    category: 'programming',
    level: 'beginner'
  });

  useEffect(() => {
    fetchProfile();
    fetchUserSkills();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get('/api/profile');
      setProfile(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile');
      setLoading(false);
    }
  };

  const fetchUserSkills = async () => {
    try {
      const response = await api.get('/api/skills/my-skills');
      setSkills(response.data);
    } catch (err) {
      console.error('Failed to load user skills');
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await api.put('/api/profile', profile);
      setProfile(response.data);
      setEditing(false);
      alert('Profile updated successfully!');
    } catch (err) {
      alert('Failed to update profile');
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    try {
      await api.post('/api/skills', newSkill);
      setNewSkill({
        name: '',
        description: '',
        category: 'programming',
        level: 'beginner'
      });
      fetchUserSkills();
      alert('Skill added successfully!');
    } catch (err) {
      alert('Failed to add skill');
    }
  };

  const handleDeleteSkill = async (skillId) => {
    if (window.confirm('Are you sure you want to delete this skill?')) {
      try {
        await api.delete(`/api/skills/${skillId}`);
        fetchUserSkills();
        alert('Skill deleted successfully');
      } catch (err) {
        alert('Failed to delete skill');
      }
    }
  };

  if (loading) return <div className="loading">Loading profile...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      
      <div className="profile-section">
        <div className="profile-header">
          <h2>Profile Information</h2>
          <button
            onClick={() => setEditing(!editing)}
            className="btn btn-primary"
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {editing ? (
          <form onSubmit={handleUpdateProfile} className="profile-form">
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={profile?.name || ''}
                onChange={(e) => setProfile({...profile, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={profile?.email || ''}
                onChange={(e) => setProfile({...profile, email: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Bio</label>
              <textarea
                value={profile?.bio || ''}
                onChange={(e) => setProfile({...profile, bio: e.target.value})}
                rows="4"
              />
            </div>
            <button type="submit" className="btn btn-success">Save Changes</button>
          </form>
        ) : (
          <div className="profile-info">
            <p><strong>Name:</strong> {profile?.name}</p>
            <p><strong>Email:</strong> {profile?.email}</p>
            <p><strong>Bio:</strong> {profile?.bio || 'No bio added yet.'}</p>
            <p><strong>Member since:</strong> {new Date(profile?.createdAt).toLocaleDateString()}</p>
          </div>
        )}
      </div>

      <div className="skills-section">
        <h2>My Skills</h2>
        
        <form onSubmit={handleAddSkill} className="add-skill-form">
          <h3>Add New Skill</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Skill Name</label>
              <input
                type="text"
                value={newSkill.name}
                onChange={(e) => setNewSkill({...newSkill, name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Category</label>
              <select
                value={newSkill.category}
                onChange={(e) => setNewSkill({...newSkill, category: e.target.value})}
              >
                <option value="programming">Programming</option>
                <option value="design">Design</option>
                <option value="marketing">Marketing</option>
                <option value="languages">Languages</option>
                <option value="music">Music</option>
                <option value="cooking">Cooking</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="form-group">
              <label>Level</label>
              <select
                value={newSkill.level}
                onChange={(e) => setNewSkill({...newSkill, level: e.target.value})}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
            </div>
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={newSkill.description}
              onChange={(e) => setNewSkill({...newSkill, description: e.target.value})}
              rows="3"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">Add Skill</button>
        </form>

        <div className="skills-list">
          {skills.length === 0 ? (
            <p className="no-skills">No skills added yet.</p>
          ) : (
            skills.map(skill => (
              <div key={skill.id} className="skill-item">
                <div className="skill-info">
                  <h4>{skill.name}</h4>
                  <p>{skill.description}</p>
                  <div className="skill-meta">
                    <span className="skill-category">{skill.category}</span>
                    <span className="skill-level">Level: {skill.level}</span>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteSkill(skill.id)}
                  className="btn btn-danger"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
