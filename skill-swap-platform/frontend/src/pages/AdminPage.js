import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './AdminPage.css';

const AdminPage = () => {
  const { api } = useAuth();
  const [users, setUsers] = useState([]);
  const [skills, setSkills] = useState([]);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('users');

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    try {
      setLoading(true);
      let response;
      
      switch (activeTab) {
        case 'users':
          response = await api.get('/api/admin/users');
          setUsers(response.data);
          break;
        case 'skills':
          response = await api.get('/api/admin/skills');
          setSkills(response.data);
          break;
        case 'requests':
          response = await api.get('/api/admin/requests');
          setRequests(response.data);
          break;
        default:
          break;
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to load data');
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await api.delete(`/api/admin/users/${userId}`);
        fetchData();
        alert('User deleted successfully');
      } catch (err) {
        alert('Failed to delete user');
      }
    }
  };

  const handleDeleteSkill = async (skillId) => {
    if (window.confirm('Are you sure you want to delete this skill?')) {
      try {
        await api.delete(`/api/admin/skills/${skillId}`);
        fetchData();
        alert('Skill deleted successfully');
      } catch (err) {
        alert('Failed to delete skill');
      }
    }
  };

  const handleDeleteRequest = async (requestId) => {
    if (window.confirm('Are you sure you want to delete this request?')) {
      try {
        await api.delete(`/api/admin/requests/${requestId}`);
        fetchData();
        alert('Request deleted successfully');
      } catch (err) {
        alert('Failed to delete request');
      }
    }
  };

  if (loading) return <div className="loading">Loading admin data...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="admin-page">
      <h1>Admin Dashboard</h1>
      
      <div className="admin-tabs">
        <button
          className={`admin-tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users ({users.length})
        </button>
        <button
          className={`admin-tab ${activeTab === 'skills' ? 'active' : ''}`}
          onClick={() => setActiveTab('skills')}
        >
          Skills ({skills.length})
        </button>
        <button
          className={`admin-tab ${activeTab === 'requests' ? 'active' : ''}`}
          onClick={() => setActiveTab('requests')}
        >
          Requests ({requests.length})
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'users' && (
          <div className="users-section">
            <h2>All Users</h2>
            <div className="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Joined</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.id}>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>
                        <span className={`role ${user.role}`}>
                          {user.role}
                        </span>
                      </td>
                      <td>{new Date(user.createdAt).toLocaleDateString()}</td>
                      <td>
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="btn btn-danger"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'skills' && (
          <div className="skills-section">
            <h2>All Skills</h2>
            <div className="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Level</th>
                    <th>Owner</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {skills.map(skill => (
                    <tr key={skill.id}>
                      <td>{skill.name}</td>
                      <td>{skill.category}</td>
                      <td>{skill.level}</td>
                      <td>{skill.owner?.name}</td>
                      <td>
                        <button
                          onClick={() => handleDeleteSkill(skill.id)}
                          className="btn btn-danger"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'requests' && (
          <div className="requests-section">
            <h2>All Requests</h2>
            <div className="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Skill</th>
                    <th>Requester</th>
                    <th>Owner</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {requests.map(request => (
                    <tr key={request.id}>
                      <td>{request.skill?.name}</td>
                      <td>{request.requester?.name}</td>
                      <td>{request.skill?.owner?.name}</td>
                      <td>
                        <span className={`status ${request.status}`}>
                          {request.status}
                        </span>
                      </td>
                      <td>{new Date(request.createdAt).toLocaleDateString()}</td>
                      <td>
                        <button
                          onClick={() => handleDeleteRequest(request.id)}
                          className="btn btn-danger"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPage;
