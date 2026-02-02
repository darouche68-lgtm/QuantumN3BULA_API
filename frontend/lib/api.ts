/**
 * API Client for Quantum-N3BULA Backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Type definitions
export interface Task {
  id: number;
  name: string;
  command: string;
  status: string;
  result: string | null;
  error: string | null;
  created_at: string;
}

export interface Log {
  id: number;
  level: string;
  message: string;
  source: string | null;
  task_id: number | null;
  agent_id: number | null;
  created_at: string;
}

export interface Agent {
  id: number;
  name: string;
  description: string | null;
  status: string;
  created_at: string;
  last_heartbeat: string | null;
}

export interface SystemStatus {
  status: string;
  uptime_seconds: number;
  active_agents: number;
  pending_tasks: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Helper function for API requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `HTTP ${response.status}`);
  }

  return response.json();
}

// Status API
export const statusApi = {
  status: (): Promise<SystemStatus> => apiRequest('/status'),
};

// Tasks API
export const tasksApi = {
  list: (): Promise<Task[]> => apiRequest('/tasks'),

  execute: (command: string, token: string): Promise<Task> =>
    apiRequest('/execute', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ command }),
    }),
};

// Logs API
export const logsApi = {
  list: (params?: { level?: string; limit?: number }): Promise<Log[]> => {
    const searchParams = new URLSearchParams();
    if (params?.level) searchParams.set('level', params.level);
    if (params?.limit) searchParams.set('limit', params.limit.toString());
    const queryString = searchParams.toString();
    return apiRequest(`/logs${queryString ? `?${queryString}` : ''}`);
  },
};

// Agents API
export const agentsApi = {
  list: (): Promise<Agent[]> => apiRequest('/agents'),

  create: (
    data: { name: string; description?: string },
    token: string
  ): Promise<Agent> =>
    apiRequest('/agents', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    }),

  delete: (id: number, token: string): Promise<void> =>
    apiRequest(`/agents/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
};

// Auth API
export const authApi = {
  // Note: login uses form-urlencoded data (OAuth2 standard) instead of JSON,
  // so we use a direct fetch call rather than the apiRequest helper
  login: (username: string, password: string): Promise<LoginResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    return fetch(`${API_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    }).then(async (response) => {
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP ${response.status}`);
      }
      return response.json();
    });
  },

  register: (data: {
    username: string;
    email: string;
    password: string;
  }): Promise<User> =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getMe: (token: string): Promise<User> =>
    apiRequest('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
};
