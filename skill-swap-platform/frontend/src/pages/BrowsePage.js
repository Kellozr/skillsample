import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './BrowsePage.css';

const BrowsePage = () => {
  const { api } = useAuth();
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      const response = await api.get('/api/skills');
      setSkills(response.data);
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
      alert('Failed to send request');
    }
  };

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         skill.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = category === 'all' || skill.category === category;
    return matchesSearch && matchesCategory;
  });

  if (loading) return <div className="loading">Loading skills...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="browse-page">
      <h1>Browse Available Skills</h1>
      
      <div className="filters">
        <input
          type="text"
          placeholder="Search skills..."
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
              <strong>Offered by:</strong> {skill.owner.name}
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

      {filteredSkills.length === 0 && (
        <div className="no-results">
          No skills found matching your criteria.
        </div>
      )}
    </div>
  );
};

export default BrowsePage;
