/**
 * API client for Quantum-N3BULA backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Type definitions based on backend Pydantic models

export interface Agent {
  id: number;
  name: string;
  description: string | null;
  status: string;
  is_active: boolean;
  last_heartbeat: string | null;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  name: string;
  command: string;
  status: string;
  result: string | null;
  error: string | null;
  agent_id: number | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
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

export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface SystemStatus {
  status: string;
  uptime_seconds: number;
  version: string;
  database_connected: boolean;
  active_agents: number;
  pending_tasks: number;
  total_logs: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Helper function for API calls
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// Status API
export const statusApi = {
  status: () => fetchAPI<SystemStatus>('/api/status'),
  ping: () => fetchAPI<{ message: string }>('/api/ping'),
};

// Tasks API
export const tasksApi = {
  list: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams(
      params ? (Object.entries(params).map(([k, v]) => [k, String(v)]) as [string, string][]) : []
    ).toString();
    return fetchAPI<Task[]>(`/api/tasks${query ? `?${query}` : ''}`);
  },
  get: (id: number) => fetchAPI<Task>(`/api/tasks/${id}`),
  create: (data: { name: string; command: string; agent_id?: number }) =>
    fetchAPI<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  execute: (data: { command: string; agent_id?: number }) =>
    fetchAPI<Task>('/api/tasks/execute', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  delete: (id: number) =>
    fetchAPI<void>(`/api/tasks/${id}`, { method: 'DELETE' }),
};

// Logs API
export const logsApi = {
  list: (params?: { skip?: number; limit?: number; level?: string }) => {
    const query = new URLSearchParams(
      params ? (Object.entries(params).map(([k, v]) => [k, String(v)]) as [string, string][]) : []
    ).toString();
    return fetchAPI<Log[]>(`/api/logs${query ? `?${query}` : ''}`);
  },
  get: (id: number) => fetchAPI<Log>(`/api/logs/${id}`),
};

// Agents API
export const agentsApi = {
  list: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams(
      params ? (Object.entries(params).map(([k, v]) => [k, String(v)]) as [string, string][]) : []
    ).toString();
    return fetchAPI<Agent[]>(`/api/agents${query ? `?${query}` : ''}`);
  },
  get: (id: number) => fetchAPI<Agent>(`/api/agents/${id}`),
  create: (data: { name: string; description?: string }) =>
    fetchAPI<Agent>('/api/agents', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  heartbeat: (id: number) =>
    fetchAPI<Agent>(`/api/agents/${id}/heartbeat`, { method: 'POST' }),
  delete: (id: number) =>
    fetchAPI<void>(`/api/agents/${id}`, { method: 'DELETE' }),
};

// Auth API
export const authApi = {
  register: (data: { username: string; email: string; password: string }) =>
    fetchAPI<User>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  login: (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    return fetch(`${API_BASE_URL}/api/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    }).then(async (response) => {
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Login failed' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }
      return response.json() as Promise<LoginResponse>;
    });
  },
  me: () => fetchAPI<User>('/api/auth/me'),
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  },
};
