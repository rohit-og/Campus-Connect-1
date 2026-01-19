'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import JobCard from '@/components/ui/JobCard';
import { Search, Filter, MapPin, Briefcase } from 'lucide-react';
import { jobsApi } from '@/lib/api';
import { Job } from '@/types/api';
import { handleApiError } from '@/lib/errors';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function JobsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [locationFilter, setLocationFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedJobs = await jobsApi.list(0, 100, searchQuery ? undefined : undefined, searchQuery || undefined);
      setJobs(fetchedJobs);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = () => {
    fetchJobs();
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return '1 day ago';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
  };

  return (
    <ProtectedRoute requiredRole="student">
      <div className="space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-bold text-base-content mb-2">Job Listings</h1>
          <p className="text-base-content/70">Find your perfect opportunity</p>
        </motion.div>

        {/* Search and Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card bg-base-100 shadow-lg"
        >
          <div className="card-body">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-base-content/50" />
                  <input
                    type="text"
                    placeholder="Search jobs..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    className="input input-bordered w-full pl-10"
                  />
                </div>
              </div>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-base-content/50" />
                <select
                  value={locationFilter}
                  onChange={(e) => setLocationFilter(e.target.value)}
                  className="select select-bordered w-full pl-10"
                >
                  <option value="">All Locations</option>
                  <option value="remote">Remote</option>
                  <option value="san-francisco">San Francisco</option>
                  <option value="new-york">New York</option>
                  <option value="austin">Austin</option>
                </select>
              </div>
              <button onClick={handleSearch} className="btn btn-primary">
                <Search className="w-5 h-5" />
                Search
              </button>
            </div>
          </div>
        </motion.div>

        {/* Error Message */}
        {error && (
          <div className="alert alert-error">
            <span>{error}</span>
            <button onClick={fetchJobs} className="btn btn-sm btn-ghost">
              Retry
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        )}

        {/* Job Listings */}
        {!isLoading && !error && (
          <>
            {jobs.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-base-content/70 text-lg">No jobs found</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {jobs
                  .filter((job) => {
                    if (locationFilter && job.location?.toLowerCase() !== locationFilter.toLowerCase()) {
                      return false;
                    }
                    return true;
                  })
                  .map((job, index) => (
                    <div
                      key={job.id}
                      onClick={() => router.push(`/student/jobs/${job.id}`)}
                      className="cursor-pointer"
                    >
                      <JobCard
                        title={job.title}
                        company={job.company}
                        location={job.location || 'Not specified'}
                        type={job.salary || 'Full-time'}
                        posted={formatDate(job.created_at)}
                        description={job.description || ''}
                        delay={index * 0.1}
                      />
                    </div>
                  ))}
              </div>
            )}
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
