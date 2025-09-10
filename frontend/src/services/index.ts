import axios from 'axios';
import type { LoginRequest, RegisterRequest, AuthResponse, ApiError } from '../types';

class ApiService {
    private api: ReturnType<typeof axios.create>;

    constructor() {
        this.api = axios.create({
            baseURL: 'http://localhost:8000/api',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Add request interceptor to include auth token
        this.api.interceptors.request.use((config) => {
            const token = localStorage.getItem('authToken');
            if (token && config.headers) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        // Add response interceptor for error handling
        this.api.interceptors.response.use(
            (response) => response,
            (error: unknown) => {
                if (error && typeof error === 'object' && 'response' in error) {
                    const axiosError = error as { response?: { status?: number } };
                    if (axiosError.response?.status === 401) {
                        // Clear token on unauthorized
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('user');
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    // Authentication endpoints
    async login(credentials: LoginRequest): Promise<AuthResponse> {
        try {
            const response = await this.api.post<AuthResponse>('/auth/login', credentials);
            return response.data;
        } catch (error: unknown) {
            throw this.handleError(error);
        }
    }

    async register(userData: RegisterRequest): Promise<AuthResponse> {
        try {
            const response = await this.api.post<AuthResponse>('/auth/register', userData);
            return response.data;
        } catch (error: unknown) {
            throw this.handleError(error);
        }
    }

    async verifyToken(): Promise<{ user_id: number; username: string; valid: boolean }> {
        try {
            const response = await this.api.get<{ user_id: number; username: string; valid: boolean }>('/auth/verify');
            return response.data;
        } catch (error: unknown) {
            throw this.handleError(error);
        }
    }

    // Health check endpoint
    async healthCheck(): Promise<{ status: string; database: string }> {
        try {
            const response = await this.api.get<{ status: string; database: string }>('/health');
            return response.data;
        } catch (error: unknown) {
            throw this.handleError(error);
        }
    }

    private handleError(error: unknown): ApiError {
        if (error && typeof error === 'object' && 'response' in error) {
            const axiosError = error as { response?: { data?: ApiError } };
            if (axiosError.response?.data) {
                return axiosError.response.data;
            }
        }

        const errorMessage = error && typeof error === 'object' && 'message' in error
            ? (error as { message: string }).message
            : 'An unexpected error occurred';

        return {
            error: 'network_error',
            message: errorMessage,
        };
    }
}

// Create and export a singleton instance
export const apiService = new ApiService();

// Export the class for testing purposes
export { ApiService };