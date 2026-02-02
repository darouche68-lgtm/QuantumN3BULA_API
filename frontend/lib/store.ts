/**
 * Zustand Store for Quantum-N3BULA Frontend
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Task, Log, Agent, SystemStatus, User } from './api';

interface AppState {
  // Auth
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  clearAuth: () => void;

  // System Status
  systemStatus: SystemStatus | null;
  setSystemStatus: (status: SystemStatus) => void;

  // Tasks
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
  addTask: (task: Task) => void;
  updateTask: (task: Task) => void;

  // Logs
  logs: Log[];
  setLogs: (logs: Log[]) => void;
  addLog: (log: Log) => void;

  // Agents
  agents: Agent[];
  setAgents: (agents: Agent[]) => void;
  addAgent: (agent: Agent) => void;
  removeAgent: (id: number) => void;

  // WebSocket state
  wsConnected: boolean;
  setWsConnected: (connected: boolean) => void;
  lastEvent: unknown;
  setLastEvent: (event: unknown) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Auth
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      clearAuth: () => set({ token: null, user: null }),

      // System Status
      systemStatus: null,
      setSystemStatus: (systemStatus) => set({ systemStatus }),

      // Tasks
      tasks: [],
      setTasks: (tasks) => set({ tasks }),
      addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
      updateTask: (updatedTask) =>
        set((state) => ({
          tasks: state.tasks.map((task) =>
            task.id === updatedTask.id ? { ...task, ...updatedTask } : task
          ),
        })),

      // Logs
      logs: [],
      setLogs: (logs) => set({ logs }),
      addLog: (log) =>
        set((state) => ({
          logs: [log, ...state.logs].slice(0, 100), // Keep last 100 logs
        })),

      // Agents
      agents: [],
      setAgents: (agents) => set({ agents }),
      addAgent: (agent) => set((state) => ({ agents: [...state.agents, agent] })),
      removeAgent: (id) =>
        set((state) => ({
          agents: state.agents.filter((agent) => agent.id !== id),
        })),

      // WebSocket state
      wsConnected: false,
      setWsConnected: (wsConnected) => set({ wsConnected }),
      lastEvent: null,
      setLastEvent: (lastEvent) => set({ lastEvent }),
    }),
    {
      name: 'quantum-nebula-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
    }
  )
);
