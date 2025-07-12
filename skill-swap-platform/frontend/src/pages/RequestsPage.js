import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './RequestsPage.css';

const RequestsPage = () => {
  const { api } = useAuth();
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('received');

  useEffect(() => {
    fetchRequests();
  }, [activeTab]);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const endpoint = activeTab === 'received' ? '/api/requests/received' : '/api/requests/sent';
      const response = await api.get(endpoint);
      setRequests(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load requests');
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (requestId, status) => {
    try {
      await api.put(`/api/requests/${requestId}`, { status });
      fetchRequests(); // Refresh the list
      alert(`Request ${status} successfully`);
    } catch (err) {
      alert('Failed to update request');
    }
  };

  const handleDeleteRequest = async (requestId) => {
    if (window.confirm('Are you sure you want to cancel this request?')) {
      try {
        await api.delete(`/api/requests/${requestId}`);
        fetchRequests(); // Refresh the list
        alert('Request cancelled successfully');
      } catch (err) {
        alert('Failed to cancel request');
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return '#f39c12';
      case 'accepted': return '#27ae60';
      case 'rejected': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  if (loading) return <div className="loading">Loading requests...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="requests-page">
      <h1>My Requests</h1>
      
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'received' ? 'active' : ''}`}
          onClick={() => setActiveTab('received')}
        >
          Received Requests ({requests.filter(r => activeTab === 'received').length})
        </button>
        <button
          className={`tab ${activeTab === 'sent' ? 'active' : ''}`}
          onClick={() => setActiveTab('sent')}
        >
          Sent Requests ({requests.filter(r => activeTab === 'sent').length})
        </button>
      </div>

      <div className="requests-list">
        {requests.length === 0 ? (
          <div className="no-requests">
            <h3>No {activeTab} requests found</h3>
            <p>
              {activeTab === 'received' 
                ? "When someone requests to learn your skills, they'll appear here."
                : "Requests you send to learn from others will appear here."
              }
            </p>
          </div>
        ) : (
          requests.map(request => (
            <div key={request.id} className="request-card">
              <div className="request-header">
                <h3>{request.skill?.name}</h3>
                <span 
                  className={`status ${request.status}`}
                  style={{ backgroundColor: getStatusColor(request.status) }}
                >
                  {request.status}
                </span>
              </div>
              
              <div className="request-details">
                <p><strong>Message:</strong> {request.message || 'No message provided'}</p>
                <p><strong>Date:</strong> {new Date(request.created_at).toLocaleDateString()}</p>
                {request.updated_at && request.updated_at !== request.created_at && (
                  <p><strong>Last Updated:</strong> {new Date(request.updated_at).toLocaleDateString()}</p>
                )}
                
                {activeTab === 'received' ? (
                  <div className="user-info">
                    <p><strong>From:</strong> {request.requester?.name}</p>
                    <p><strong>Email:</strong> {request.requester?.email}</p>
                    {request.requester?.bio && (
                      <p><strong>About:</strong> {request.requester.bio}</p>
                    )}
                  </div>
                ) : (
                  <div className="user-info">
                    <p><strong>To:</strong> {request.skill?.owner?.name}</p>
                    <p><strong>Skill Category:</strong> {request.skill?.category}</p>
                    <p><strong>Skill Level:</strong> {request.skill?.level}</p>
                  </div>
                )}
              </div>

              <div className="request-actions">
                {activeTab === 'received' && request.status === 'pending' && (
                  <>
                    <button
                      onClick={() => handleUpdateStatus(request.id, 'accepted')}
                      className="btn btn-success"
                    >
                      Accept
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(request.id, 'rejected')}
                      className="btn btn-danger"
                    >
                      Reject
                    </button>
                  </>
                )}
                
                {activeTab === 'sent' && request.status === 'pending' && (
                  <button
                    onClick={() => handleDeleteRequest(request.id)}
                    className="btn btn-danger"
                  >
                    Cancel Request
                  </button>
                )}

                {request.status === 'accepted' && (
                  <div className="contact-info">
                    <p style={{ color: '#27ae60', fontWeight: 'bold' }}>
                      ✅ Request accepted! You can now contact each other to arrange learning sessions.
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default RequestsPage;