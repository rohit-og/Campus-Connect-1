// src/components/student/JobCard.jsx

const JobCard = ({ job, onApplyClick }) => {
  return (
    <div className="p-4 border-2 border-gray-200 rounded-lg hover:border-indigo-300 hover:shadow-md transition">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h4 className="font-bold text-lg text-gray-900">{job.role}</h4>
          <p className="text-sm text-gray-600">{job.company}</p>
          <p className="text-xs text-gray-500 mt-1">{job.location} • {job.type}</p>
        </div>
        <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
          {job.match} Match
        </span>
      </div>
      
      <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200">
        <span className="text-sm font-medium text-gray-700">{job.salary}</span>
        <button
          onClick={() => onApplyClick(job)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
        >
          View Details →
        </button>
      </div>
    </div>
  );
};

export default JobCard;
