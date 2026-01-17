// src/data/jobsData.js
// Mock data - Your AI engineer will replace this with real API data

export const jobsData = [
  {
    id: 1,
    company: "Tech Corp",
    role: "Software Engineer",
    match: "95%",
    location: "Bangalore, India",
    type: "Full-time",
    experience: "0-2 years",
    salary: "₹8-12 LPA",
    postedDate: "2024-01-15",
    deadline: "2024-02-28",
    openings: 5,
    description: `We are looking for a talented Software Engineer to join our dynamic team. You will be working on cutting-edge technologies and building scalable applications that serve millions of users.

Key Responsibilities:
• Design, develop, and maintain web applications
• Collaborate with cross-functional teams
• Write clean, maintainable code
• Participate in code reviews
• Contribute to architectural decisions

What We Offer:
• Competitive salary and benefits
• Flexible work hours
• Learning and development opportunities
• Modern tech stack
• Great work culture`,
    
    requirements: [
      "Bachelor's degree in Computer Science or related field",
      "Strong problem-solving skills",
      "Good communication skills",
      "Team player with collaborative mindset",
      "Willingness to learn new technologies"
    ],

    interviewProcess: [
      {
        stage: 1,
        name: "Online Assessment",
        description: "Aptitude and coding test (90 minutes)",
        duration: "90 mins"
      },
      {
        stage: 2,
        name: "Technical Round 1",
        description: "DSA and problem-solving (60 minutes)",
        duration: "60 mins"
      },
      {
        stage: 3,
        name: "Technical Round 2",
        description: "System design and project discussion (60 minutes)",
        duration: "60 mins"
      },
      {
        stage: 4,
        name: "HR Round",
        description: "Cultural fit and salary discussion (30 minutes)",
        duration: "30 mins"
      }
    ],

    scheduleDetails: {
      date: "February 15, 2024",
      time: "10:00 AM IST",
      mode: "Online (Microsoft Teams)",
      duration: "Full Day"
    },

    requiredSkills: [
      {
        name: "React.js",
        studentLevel: 90,
        requiredLevel: 85,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "Node.js",
        studentLevel: 75,
        requiredLevel: 70,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "JavaScript",
        studentLevel: 85,
        requiredLevel: 80,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "System Design",
        studentLevel: 60,
        requiredLevel: 75,
        priority: "Must Have",
        gap: 15
      },
      {
        name: "AWS",
        studentLevel: 30,
        requiredLevel: 70,
        priority: "Good to Have",
        gap: 40
      },
      {
        name: "Docker",
        studentLevel: 0,
        requiredLevel: 60,
        priority: "Good to Have",
        gap: 60
      }
    ],

    companyInfo: {
      name: "Tech Corp",
      website: "www.techcorp.com",
      size: "1000-5000 employees",
      industry: "Technology, Software",
      description: "Leading technology company building innovative solutions"
    }
  },
  {
    id: 2,
    company: "InnovateLabs",
    role: "Frontend Developer",
    match: "88%",
    location: "Remote",
    type: "Full-time",
    experience: "0-1 years",
    salary: "₹6-10 LPA",
    postedDate: "2024-01-20",
    deadline: "2024-03-15",
    openings: 3,
    description: `Join our creative team as a Frontend Developer and help us build beautiful, responsive user interfaces. Work with modern technologies and frameworks in a fully remote environment.

Key Responsibilities:
• Develop responsive web applications
• Implement pixel-perfect designs
• Optimize application performance
• Collaborate with designers and backend developers
• Write reusable components

What We Offer:
• Remote work flexibility
• Health insurance
• Annual bonuses
• Latest MacBook Pro
• Quarterly team outings`,
    
    requirements: [
      "Strong knowledge of HTML, CSS, JavaScript",
      "Experience with React.js",
      "Understanding of responsive design",
      "Portfolio of previous work",
      "Attention to detail"
    ],

    interviewProcess: [
      {
        stage: 1,
        name: "Portfolio Review",
        description: "Review of submitted projects and portfolio",
        duration: "N/A"
      },
      {
        stage: 2,
        name: "Coding Challenge",
        description: "Take-home assignment (48 hours)",
        duration: "48 hours"
      },
      {
        stage: 3,
        name: "Technical Interview",
        description: "Discussion on assignment and technical concepts",
        duration: "45 mins"
      },
      {
        stage: 4,
        name: "Culture Fit",
        description: "Meet the team and discuss work culture",
        duration: "30 mins"
      }
    ],

    scheduleDetails: {
      date: "February 20, 2024",
      time: "2:00 PM IST",
      mode: "Online (Google Meet)",
      duration: "Half Day"
    },

    requiredSkills: [
      {
        name: "React.js",
        studentLevel: 90,
        requiredLevel: 90,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "CSS/Tailwind",
        studentLevel: 85,
        requiredLevel: 80,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "JavaScript",
        studentLevel: 85,
        requiredLevel: 85,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "TypeScript",
        studentLevel: 40,
        requiredLevel: 70,
        priority: "Must Have",
        gap: 30
      },
      {
        name: "UI/UX Design",
        studentLevel: 50,
        requiredLevel: 65,
        priority: "Good to Have",
        gap: 15
      }
    ],

    companyInfo: {
      name: "InnovateLabs",
      website: "www.innovatelabs.io",
      size: "50-200 employees",
      industry: "Design, Technology",
      description: "Creative agency specializing in web and mobile applications"
    }
  },
  {
    id: 3,
    company: "DataSystems",
    role: "ML Engineer",
    match: "82%",
    location: "Hyderabad, India",
    type: "Full-time",
    experience: "0-2 years",
    salary: "₹10-15 LPA",
    postedDate: "2024-01-10",
    deadline: "2024-02-25",
    openings: 2,
    description: `We're seeking a passionate ML Engineer to join our AI/ML team. Work on exciting projects involving machine learning, deep learning, and data science.

Key Responsibilities:
• Develop and deploy ML models
• Work with large datasets
• Implement data pipelines
• Collaborate with data scientists
• Optimize model performance

What We Offer:
• Cutting-edge ML projects
• GPU workstations
• Conference sponsorships
• Research paper publications
• Mentorship from industry experts`,
    
    requirements: [
      "Strong foundation in mathematics and statistics",
      "Knowledge of Python and ML libraries",
      "Understanding of ML algorithms",
      "Experience with data preprocessing",
      "Problem-solving mindset"
    ],

    interviewProcess: [
      {
        stage: 1,
        name: "Technical Screening",
        description: "ML concepts and Python coding",
        duration: "60 mins"
      },
      {
        stage: 2,
        name: "ML Assignment",
        description: "Real-world ML problem solving",
        duration: "3 days"
      },
      {
        stage: 3,
        name: "Technical Deep Dive",
        description: "Assignment discussion and advanced ML topics",
        duration: "90 mins"
      },
      {
        stage: 4,
        name: "Final Round",
        description: "Meet the team and HR discussion",
        duration: "45 mins"
      }
    ],

    scheduleDetails: {
      date: "February 25, 2024",
      time: "11:00 AM IST",
      mode: "Hybrid (Initial rounds online)",
      duration: "2 Days"
    },

    requiredSkills: [
      {
        name: "Python",
        studentLevel: 80,
        requiredLevel: 85,
        priority: "Must Have",
        gap: 5
      },
      {
        name: "Machine Learning",
        studentLevel: 70,
        requiredLevel: 80,
        priority: "Must Have",
        gap: 10
      },
      {
        name: "TensorFlow/PyTorch",
        studentLevel: 50,
        requiredLevel: 75,
        priority: "Must Have",
        gap: 25
      },
      {
        name: "Data Structures",
        studentLevel: 75,
        requiredLevel: 70,
        priority: "Must Have",
        gap: 0
      },
      {
        name: "SQL",
        studentLevel: 60,
        requiredLevel: 70,
        priority: "Good to Have",
        gap: 10
      },
      {
        name: "Deep Learning",
        studentLevel: 45,
        requiredLevel: 70,
        priority: "Good to Have",
        gap: 25
      }
    ],

    companyInfo: {
      name: "DataSystems",
      website: "www.datasystems.ai",
      size: "500-1000 employees",
      industry: "AI/ML, Data Science",
      description: "Leading AI solutions provider for enterprise clients"
    }
  }
];