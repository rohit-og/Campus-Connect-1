// src/pages/JobDetailsPage.jsx - IMPROVED VERSION
import {
    ArrowLeft,
    Award,
    Briefcase,
    Building2,
    Calendar,
    CheckCircle,
    Clock,
    DollarSign,
    Globe,
    MapPin,
    Target,
    TrendingUp,
    Users,
    Video
} from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import DashboardHeader from '../components/common/DashboardHeader';
import SkillGapCard from '../components/student/SkillGapCard';
import { PAGES } from '../data/constants';

const JobDetailsPage = ({ job, onNavigate, onApply }) => {
  const [isApplied, setIsApplied] = useState(false);

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Job not found</h2>
          <button
            onClick={() => onNavigate(PAGES.DASHBOARD)}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const handleApply = () => {
    const loadingToast = toast.loading('Submitting your application...');

    setTimeout(() => {
      toast.dismiss(loadingToast);
      
      toast.success(
        (t) => (
          <div className="flex flex-col gap-2">
            <div className="font-bold text-lg">Application Submitted! 🎉</div>
            <div className="text-sm">Your application for {job.role} at {job.company} has been submitted successfully.</div>
            <div className="text-xs text-green-200 mt-1">You'll receive updates via email.</div>
          </div>
        ),
        {
          duration: 5000,
          style: {
            background: '#10b981',
            color: '#fff',
            minWidth: '350px',
          },
        }
      );

      setIsApplied(true);
      onApply(job.id);

      setTimeout(() => {
        onNavigate(PAGES.DASHBOARD);
      }, 2000);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <DashboardHeader 
        title="Job Details" 
        onBackToHome={() => onNavigate(PAGES.LANDING)}
      />

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Back Button */}
        <button
          onClick={() => onNavigate(PAGES.DASHBOARD)}
          className="flex items-center gap-2 text-gray-600 hover:text-indigo-600 mb-6 transition font-medium"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Dashboard
        </button>

        {/* Job Header Card */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-8 mb-6 text-white">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                  <Building2 className="w-8 h-8" />
                </div>
                <div>
                  <h1 className="text-3xl md:text-4xl font-bold">{job.role}</h1>
                  <p className="text-xl text-indigo-100">{job.company}</p>
                </div>
              </div>
              
              {/* Quick Info Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-3 py-2">
                  <MapPin className="w-4 h-4" />
                  <span className="text-sm">{job.location}</span>
                </div>
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-3 py-2">
                  <Briefcase className="w-4 h-4" />
                  <span className="text-sm">{job.type}</span>
                </div>
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-3 py-2">
                  <Clock className="w-4 h-4" />
                  <span className="text-sm">{job.experience}</span>
                </div>
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-3 py-2">
                  <DollarSign className="w-4 h-4" />
                  <span className="text-sm font-semibold">{job.salary}</span>
                </div>
              </div>
            </div>

            {/* Match Badge */}
            <div className="flex flex-col items-center gap-2 bg-white/20 backdrop-blur-sm rounded-2xl px-6 py-4">
              <Award className="w-8 h-8" />
              <span className="text-3xl font-bold">{job.match}</span>
              <span className="text-sm text-indigo-100">Match Score</span>
            </div>
          </div>

          {/* Deadline & Openings */}
          <div className="flex flex-wrap gap-4 mt-6 pt-6 border-t border-white/20">
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <Calendar className="w-4 h-4" />
              <span className="text-sm">Deadline: <strong>{job.deadline}</strong></span>
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <Users className="w-4 h-4" />
              <span className="text-sm">Openings: <strong>{job.openings}</strong></span>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column - 2/3 width */}
          <div className="lg:col-span-2 space-y-6">
            {/* Job Description */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Briefcase className="w-6 h-6 text-indigo-600" />
                Job Description
              </h2>
              <div className="text-gray-700 whitespace-pre-line leading-relaxed">
                {job.description}
              </div>
            </div>

            {/* Requirements */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-green-600" />
                Requirements
              </h2>
              <ul className="space-y-3">
                {job.requirements.map((req, index) => (
                  <li key={index} className="flex items-start gap-3 bg-gray-50 rounded-lg p-3">
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{req}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Interview Process */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Target className="w-6 h-6 text-indigo-600" />
                Interview Process
              </h2>
              <div className="relative">
                {/* Vertical Line */}
                <div className="absolute left-5 top-8 bottom-8 w-0.5 bg-gradient-to-b from-indigo-600 to-purple-600"></div>
                
                <div className="space-y-6">
                  {job.interviewProcess.map((stage) => (
                    <div key={stage.stage} className="relative flex gap-4">
                      {/* Stage Number Circle */}
                      <div className="relative z-10 flex-shrink-0">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 text-white flex items-center justify-center font-bold shadow-lg">
                          {stage.stage}
                        </div>
                      </div>
                      
                      {/* Stage Content */}
                      <div className="flex-1 bg-gradient-to-br from-gray-50 to-white p-4 rounded-lg border border-gray-200 shadow-sm">
                        <h3 className="font-bold text-gray-900 mb-1 text-lg">{stage.name}</h3>
                        <p className="text-sm text-gray-600 mb-2">{stage.description}</p>
                        <div className="flex items-center gap-2 text-xs text-indigo-600 font-semibold bg-indigo-50 rounded-full px-3 py-1 w-fit">
                          <Clock className="w-3 h-3" />
                          {stage.duration}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Skill Gap Analysis - Full Width */}
            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl shadow-lg p-6 border-2 border-purple-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-purple-600" />
                Skill Gap Analysis
              </h2>
              <p className="text-sm text-gray-600 mb-6">
                Compare your skills with this job's requirements. Focus on gaps to boost your chances!
              </p>
              <SkillGapCard skills={job.requiredSkills} />
            </div>
          </div>

          {/* Right Sidebar - 1/3 width */}
          <div className="space-y-6">
            {/* Schedule Card */}
            <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl shadow-lg p-6 border-2 border-orange-200 sticky top-4">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Calendar className="w-6 h-6 text-orange-600" />
                Interview Schedule
              </h2>
              <div className="space-y-3">
                <div className="flex items-center gap-3 bg-white rounded-lg p-3 shadow-sm">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <Calendar className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Date</p>
                    <p className="font-bold text-gray-900">{job.scheduleDetails.date}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 bg-white rounded-lg p-3 shadow-sm">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Clock className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Time</p>
                    <p className="font-bold text-gray-900">{job.scheduleDetails.time}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 bg-white rounded-lg p-3 shadow-sm">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Video className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Mode</p>
                    <p className="font-bold text-gray-900">{job.scheduleDetails.mode}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 bg-white rounded-lg p-3 shadow-sm">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Clock className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Duration</p>
                    <p className="font-bold text-gray-900">{job.scheduleDetails.duration}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Company Info Card */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Building2 className="w-6 h-6 text-indigo-600" />
                About Company
              </h2>
              <div className="space-y-4">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-600 mb-1">Company Name</p>
                  <p className="font-bold text-gray-900">{job.companyInfo.name}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-600 mb-1">Industry</p>
                  <p className="font-semibold text-gray-900">{job.companyInfo.industry}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-600 mb-1">Company Size</p>
                  <p className="font-semibold text-gray-900">{job.companyInfo.size}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-600 mb-2">Website</p>
                  <a 
                    href={`https://${job.companyInfo.website}`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-indigo-600 hover:text-indigo-700 font-medium"
                  >
                    <Globe className="w-4 h-4" />
                    {job.companyInfo.website}
                  </a>
                </div>
                <div className="pt-3 border-t">
                  <p className="text-sm text-gray-700">{job.companyInfo.description}</p>
                </div>
              </div>
            </div>

            {/* Apply Button Card */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-xl p-6">
              <button
                onClick={handleApply}
                disabled={isApplied}
                className={`w-full py-4 rounded-xl font-bold text-lg transition transform hover:scale-105 ${
                  isApplied
                    ? 'bg-green-500 cursor-not-allowed text-white'
                    : 'bg-white text-indigo-600 hover:bg-gray-50 shadow-lg'
                }`}
              >
                {isApplied ? (
                  <span className="flex items-center justify-center gap-2">
                    <CheckCircle className="w-6 h-6" />
                    Applied Successfully
                  </span>
                ) : (
                  'Apply Now →'
                )}
              </button>

              {!isApplied && (
                <p className="text-xs text-white/80 text-center mt-3">
                  ✨ One click away from your dream job!
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetailsPage;