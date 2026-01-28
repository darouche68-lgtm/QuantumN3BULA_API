/**
 * Zustand store for global state management
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Agent, Task, Log, User, SystemStatus } from './api';

interface AppStore {
  // Auth state
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  clearAuth: () => void;

  // System status
  systemStatus: SystemStatus | null;
  setSystemStatus: (status: SystemStatus) => void;

  // WebSocket state
  wsConnected: boolean;
  setWsConnected: (connected: boolean) => void;
  lastEvent: unknown;
  setLastEvent: (event: unknown) => void;

  // Tasks
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
  addTask: (task: Task) => void;
  updateTask: (id: number, task: Partial<Task>) => void;
  removeTask: (id: number) => void;

  // Logs
  logs: Log[];
  setLogs: (logs: Log[]) => void;
  addLog: (log: Log) => void;

  // Agents
  agents: Agent[];
  setAgents: (agents: Agent[]) => void;
  addAgent: (agent: Agent) => void;
  updateAgent: (id: number, agent: Partial<Agent>) => void;
  removeAgent: (id: number) => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      // Auth state
      token: null,
      user: null,
      setAuth: (token, user) => {
        if (typeof window !== 'undefined') {
          localStorage.setItem('token', token);
        }
        set({ token, user });
      },
      clearAuth: () => {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('token');
        }
        set({ token: null, user: null });
      },

      // System status
      systemStatus: null,
      setSystemStatus: (status) => set({ systemStatus: status }),

      // WebSocket state
      wsConnected: false,
      setWsConnected: (connected) => set({ wsConnected: connected }),
      lastEvent: null,
      setLastEvent: (event) => set({ lastEvent: event }),

      // Tasks
      tasks: [],
      setTasks: (tasks) => set({ tasks }),
      addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
      updateTask: (id, updatedTask) =>
        set((state) => ({
          tasks: state.tasks.map((task) =>
            task.id === id ? { ...task, ...updatedTask } : task
          ),
        })),
      removeTask: (id) =>
        set((state) => ({
          tasks: state.tasks.filter((task) => task.id !== id),
        })),

      // Logs
      logs: [],
      setLogs: (logs) => set({ logs }),
      addLog: (log) => set((state) => ({ logs: [log, ...state.logs] })),

      // Agents
      agents: [],
      setAgents: (agents) => set({ agents }),
      addAgent: (agent) => set((state) => ({ agents: [...state.agents, agent] })),
      updateAgent: (id, updatedAgent) =>
        set((state) => ({
          agents: state.agents.map((agent) =>
            agent.id === id ? { ...agent, ...updatedAgent } : agent
          ),
        })),
      removeAgent: (id) =>
        set((state) => ({
          agents: state.agents.filter((agent) => agent.id !== id),
        })),
    }),
    {
      name: 'quantum-nebula-store',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
    }
  )
);
