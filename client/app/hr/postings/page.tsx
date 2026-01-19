'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, Edit, Trash2, Eye, Briefcase, MapPin, Clock } from 'lucide-react';
import { jobsApi } from '@/lib/api';
import { Job } from '@/types/api';
import { handleApiError } from '@/lib/errors';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

interface JobPosting {
  id: number;
  title: string;
  location: string;
  type: string;
  status: 'active' | 'draft' | 'closed';
  applications: number;
  postedDate: string;
}

export default function PostingsPage() {
  const [showModal, setShowModal] = useState(false);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newJob, setNewJob] = useState({
    title: '',
    location: '',
    type: 'Full-time',
    description: '',
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedJobs = await jobsApi.list(0, 100);
      setJobs(fetchedJobs);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  };

  // Convert jobs to postings format
  const postings: JobPosting[] = jobs.map((job) => ({
    id: job.id,
    title: job.title,
    location: job.location || 'Not specified',
    type: job.salary || 'Full-time',
    status: 'active' as const,
    applications: 0, // TODO: Get from applications API
    postedDate: job.created_at,
  }));

  const handleCreateJob = async () => {
    if (!newJob.title || !newJob.description) {
      alert('Please fill in all required fields');
      return;
    }
    try {
      await jobsApi.create({
        title: newJob.title,
        company: 'Your Company', // TODO: Get from user profile
        location: newJob.location,
        description: newJob.description,
        salary: newJob.type,
        requirements_json: {},
      });
      setShowModal(false);
      setNewJob({ title: '', location: '', type: 'Full-time', description: '' });
      fetchJobs();
    } catch (err) {
      alert('Failed to create job: ' + handleApiError(err));
    }
  };

  const handleDeleteJob = async (jobId: number) => {
    if (confirm('Are you sure you want to delete this job posting?')) {
      try {
        await jobsApi.delete(jobId);
        fetchJobs();
      } catch (err) {
        alert('Failed to delete job: ' + handleApiError(err));
      }
    }
  };

  const getStatusBadge = (status: JobPosting['status']) => {
    const badges = {
      active: 'badge-success',
      draft: 'badge-warning',
      closed: 'badge-error',
    };
    return badges[status];
  };

  return (
    <ProtectedRoute requiredRole="hr">
      <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-bold text-base-content mb-2">Job Postings</h1>
          <p className="text-base-content/70">Manage your job openings</p>
        </motion.div>
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          onClick={() => setShowModal(true)}
          className="btn btn-primary"
        >
          <Plus className="w-5 h-5 mr-2" />
          Create Posting
        </motion.button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button onClick={fetchJobs} className="btn btn-sm btn-ghost">Retry</button>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      )}

      {/* Postings Grid */}
      {!isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {postings.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <p className="text-base-content/70">No job postings yet. Create your first one!</p>
            </div>
          ) : (
            postings.map((posting, index) => (
          <motion.div
            key={posting.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow"
          >
            <div className="card-body">
              <div className="flex justify-between items-start mb-2">
                <h3 className="card-title text-xl text-base-content">{posting.title}</h3>
                <div className={`badge ${getStatusBadge(posting.status)}`}>
                  {posting.status}
                </div>
              </div>
              <div className="space-y-2 text-sm text-base-content/70 mb-4">
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>{posting.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Briefcase className="w-4 h-4" />
                  <span>{posting.type}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span>Posted: {new Date(posting.postedDate).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm text-base-content/70">Applications</p>
                  <p className="text-2xl font-bold text-primary">{posting.applications}</p>
                </div>
              </div>
              <div className="card-actions justify-end">
                <button className="btn btn-ghost btn-sm">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="btn btn-ghost btn-sm">
                  <Edit className="w-4 h-4" />
                </button>
                <button 
                  className="btn btn-ghost btn-sm text-error"
                  onClick={() => handleDeleteJob(posting.id)}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
            ))
          )}
        </div>
      )}

      {/* Create Posting Modal */}
      {showModal && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg mb-4">Create New Job Posting</h3>
            <div className="space-y-4">
              <div>
                <label className="label">
                  <span className="label-text">Job Title</span>
                </label>
                <input 
                  type="text" 
                  className="input input-bordered w-full"
                  value={newJob.title}
                  onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
                />
              </div>
              <div>
                <label className="label">
                  <span className="label-text">Location</span>
                </label>
                <input 
                  type="text" 
                  className="input input-bordered w-full"
                  value={newJob.location}
                  onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
                />
              </div>
              <div>
                <label className="label">
                  <span className="label-text">Job Type</span>
                </label>
                <select 
                  className="select select-bordered w-full"
                  value={newJob.type}
                  onChange={(e) => setNewJob({ ...newJob, type: e.target.value })}
                >
                  <option>Full-time</option>
                  <option>Part-time</option>
                  <option>Contract</option>
                  <option>Internship</option>
                </select>
              </div>
              <div>
                <label className="label">
                  <span className="label-text">Description</span>
                </label>
                <textarea 
                  className="textarea textarea-bordered w-full h-32"
                  value={newJob.description}
                  onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
                />
              </div>
            </div>
            <div className="modal-action">
              <button 
                onClick={() => {
                  setShowModal(false);
                  setNewJob({ title: '', location: '', type: 'Full-time', description: '' });
                }} 
                className="btn btn-ghost"
              >
                Cancel
              </button>
              <button 
                onClick={handleCreateJob}
                className="btn btn-primary"
              >
                Create Posting
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </ProtectedRoute>
  );
}
