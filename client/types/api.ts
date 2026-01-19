// TypeScript types matching backend schemas

export enum UserRole {
  STUDENT = "student",
  RECRUITER = "recruiter",
  ADMIN = "admin",
}

export interface User {
  id: number;
  email: string;
  role: UserRole;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserCreate {
  email: string;
  password: string;
  role: UserRole;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  description?: string;
  location?: string;
  salary?: string;
  requirements_json: Record<string, any>;
  created_by: number;
  created_at: string;
  updated_at?: string;
}

export interface JobCreate {
  title: string;
  company: string;
  description?: string;
  location?: string;
  salary?: string;
  requirements_json: Record<string, any>;
}

export interface Application {
  id: number;
  job_id: number;
  candidate_id: number;
  status: ApplicationStatus;
  applied_at: string;
  updated_at?: string;
}

export enum ApplicationStatus {
  PENDING = "pending",
  REVIEWING = "reviewing",
  SHORTLISTED = "shortlisted",
  REJECTED = "rejected",
  ACCEPTED = "accepted",
}

export interface Candidate {
  id: number;
  user_id: number;
  name: string;
  email: string;
  phone?: string;
  skills_json?: string[];
  resume_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface ApiError {
  detail: string;
}

export interface JobSearchRequest {
  query: string;
  student_skills: string[];
  top_k?: number;
}

export interface JobSearchResponse {
  job_id: number;
  title: string;
  company: string;
  location?: string;
  salary?: string;
  match_score: number;
  application_status: string;
  missing_skills: string[];
  matched_skills: string[];
  message: string;
  required_skills: string[];
}
