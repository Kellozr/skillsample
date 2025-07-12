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
      alert(`Request ${status}`);
    } catch (err) {
      alert('Failed to update request');
    }
  };

  const handleDeleteRequest = async (requestId) => {
    if (window.confirm('Are you sure you want to delete this request?')) {
      try {
        await api.delete(`/api/requests/${requestId}`);
        fetchRequests(); // Refresh the list
        alert('Request deleted successfully');
      } catch (err) {
        alert('Failed to delete request');
      }
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
          Received Requests
        </button>
        <button
          className={`tab ${activeTab === 'sent' ? 'active' : ''}`}
          onClick={() => setActiveTab('sent')}
        >
          Sent Requests
        </button>
      </div>

      <div className="requests-list">
        {requests.length === 0 ? (
          <div className="no-requests">
            No {activeTab} requests found.
          </div>
        ) : (
          requests.map(request => (
            <div key={request.id} className="request-card">
              <div className="request-header">
                <h3>{request.skill.name}</h3>
                <span className={`status ${request.status}`}>
                  {request.status}
                </span>
              </div>
              
              <div className="request-details">
                <p><strong>Message:</strong> {request.message}</p>
                <p><strong>Date:</strong> {new Date(request.createdAt).toLocaleDateString()}</p>
                
                {activeTab === 'received' ? (
                  <div className="user-info">
                    <p><strong>From:</strong> {request.requester.name}</p>
                    <p><strong>Email:</strong> {request.requester.email}</p>
                  </div>
                ) : (
                  <div className="user-info">
                    <p><strong>To:</strong> {request.skill.owner.name}</p>
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
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default RequestsPage;
