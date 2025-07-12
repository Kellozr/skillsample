import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './BrowsePage.css';

const BrowsePage = () => {
  const { api, user } = useAuth();
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');
  const [level, setLevel] = useState('all');

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      const response = await api.get('/api/skills');
      // Filter out user's own skills
      const filteredSkills = response.data.filter(skill => skill.owner_id !== user?.id);
      setSkills(filteredSkills);
      setLoading(false);
    } catch (err) {
      setError('Failed to load skills');
      setLoading(false);
    }
  };

  const handleRequestSkill = async (skillId) => {
    try {
      await api.post('/api/requests', {
        skillId,
        message: 'I would like to learn this skill!'
      });
      alert('Request sent successfully!');
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to send request';
      alert(errorMessage);
    }
  };

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         skill.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         skill.owner?.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = category === 'all' || skill.category === category;
    const matchesLevel = level === 'all' || skill.level === level;
    return matchesSearch && matchesCategory && matchesLevel;
  });

  if (loading) return <div className="loading">Loading skills...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="browse-page">
      <h1>Browse Available Skills</h1>
      
      <div className="filters">
        <input
          type="text"
          placeholder="Search skills, descriptions, or teachers..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="category-select"
        >
          <option value="all">All Categories</option>
          <option value="programming">Programming</option>
          <option value="design">Design</option>
          <option value="marketing">Marketing</option>
          <option value="languages">Languages</option>
          <option value="music">Music</option>
          <option value="cooking">Cooking</option>
          <option value="other">Other</option>
        </select>
        <select
          value={level}
          onChange={(e) => setLevel(e.target.value)}
          className="category-select"
        >
          <option value="all">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
          <option value="expert">Expert</option>
        </select>
      </div>

      <div className="results-info">
        <p>Found {filteredSkills.length} skill{filteredSkills.length !== 1 ? 's' : ''}</p>
      </div>

      <div className="skills-grid">
        {filteredSkills.map(skill => (
          <div key={skill.id} className="skill-card">
            <h3>{skill.name}</h3>
            <p className="skill-description">{skill.description}</p>
            <div className="skill-meta">
              <span className="skill-category">{skill.category}</span>
              <span className="skill-level">Level: {skill.level}</span>
            </div>
            <div className="skill-owner">
              <strong>Offered by:</strong> {skill.owner?.name}
              {skill.owner?.bio && (
                <p className="owner-bio">{skill.owner.bio}</p>
              )}
            </div>
            <div className="skill-date">
              Added: {new Date(skill.created_at).toLocaleDateString()}
            </div>
            <button
              onClick={() => handleRequestSkill(skill.id)}
              className="request-btn"
            >
              Request to Learn
            </button>
          </div>
        ))}
      </div>

      {filteredSkills.length === 0 && !loading && (
        <div className="no-results">
          {skills.length === 0 ? (
            <div>
              <h3>No skills available yet</h3>
              <p>Be the first to add a skill and start sharing knowledge!</p>
            </div>
          ) : (
            <div>
              <h3>No skills found matching your criteria</h3>
              <p>Try adjusting your search terms or filters.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default BrowsePage;