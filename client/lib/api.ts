import { Token, User, ApiError, Job, JobCreate, JobSearchResponse } from '@/types/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
};

// Set token in localStorage
export const setToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_token', token);
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_token');
};

// Get user from localStorage
export const getUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('auth_user');
  return userStr ? JSON.parse(userStr) : null;
};

// Set user in localStorage
export const setUser = (user: User): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_user', JSON.stringify(user));
};

// Remove user from localStorage
export const removeUser = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_user');
};

// API Error class
export class ApiException extends Error {
  constructor(
    public status: number,
    public message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiException';
  }
}

// Base fetch wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Merge existing headers if they're a plain object
  if (options.headers) {
    if (options.headers instanceof Headers) {
      options.headers.forEach((value, key) => {
        headers[key] = value;
      });
    } else if (Array.isArray(options.headers)) {
      options.headers.forEach(([key, value]) => {
        headers[key] = value;
      });
    } else {
      Object.assign(headers, options.headers);
    }
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${API_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: headers as HeadersInit,
    });

    // Handle empty responses (like 204 No Content)
    if (response.status === 204) {
      return null as T;
    }

    const data = await response.json();

    if (!response.ok) {
      const errorMessage = data.detail || data.message || `HTTP ${response.status}`;
      throw new ApiException(response.status, errorMessage, data);
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiException) {
      throw error;
    }
    // Network or other errors
    throw new ApiException(0, error instanceof Error ? error.message : 'Network error');
  }
}

// Auth API
export const authApi = {
  login: async (email: string, password: string): Promise<Token> => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const data = await response.json();
      const errorMessage = data.detail || data.message || `HTTP ${response.status}`;
      throw new ApiException(response.status, errorMessage, data);
    }

    return response.json();
  },

  register: async (email: string, password: string, role: 'student' | 'recruiter'): Promise<User> => {
    return apiRequest<User>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, role }),
    });
  },

  getMe: async (): Promise<User> => {
    return apiRequest<User>('/api/v1/auth/me');
  },

  refreshToken: async (): Promise<Token> => {
    return apiRequest<Token>('/api/v1/auth/refresh', {
      method: 'POST',
    });
  },
};

// Jobs API
export const jobsApi = {
  list: async (skip = 0, limit = 100, company?: string, title?: string): Promise<Job[]> => {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    if (company) params.append('company', company);
    if (title) params.append('title', title);
    
    return apiRequest<Job[]>(`/api/v1/jobs?${params.toString()}`);
  },

  get: async (jobId: number): Promise<Job> => {
    return apiRequest<Job>(`/api/v1/jobs/${jobId}`);
  },

  create: async (job: JobCreate): Promise<Job> => {
    return apiRequest<Job>('/api/v1/jobs', {
      method: 'POST',
      body: JSON.stringify(job),
    });
  },

  update: async (jobId: number, job: Partial<JobCreate>): Promise<Job> => {
    return apiRequest<Job>(`/api/v1/jobs/${jobId}`, {
      method: 'PUT',
      body: JSON.stringify(job),
    });
  },

  delete: async (jobId: number): Promise<void> => {
    return apiRequest<void>(`/api/v1/jobs/${jobId}`, {
      method: 'DELETE',
    });
  },
};

// Student API
export const studentApi = {
  searchJobs: async (query: string, studentSkills: string[], topK = 10): Promise<JobSearchResponse[]> => {
    return apiRequest<JobSearchResponse[]>('/api/v1/student/jobs/search', {
      method: 'POST',
      body: JSON.stringify({
        query,
        student_skills: studentSkills,
        top_k: topK,
      }),
    });
  },
};
