// User data interfaces
export interface User {
  id: number;
  username: string;
  email: string;
}

// Authentication request interfaces
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

// Authentication response interfaces
export interface AuthResponse {
  user_id: number;
  username: string;
  token: string;
}

// API error interface
export interface ApiError {
  error: string;
  message: string;
  details?: {
    field?: string;
    code?: string;
  };
}

// Form validation interfaces
export interface FormErrors {
  [key: string]: string;
}