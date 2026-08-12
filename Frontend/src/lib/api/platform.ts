import { api } from "./client";
import type {
  ApiResponse,
  AuditLog,
  Notification,
  PaginatedResponse,
  Plugin,
  SearchResult,
  Workflow,
} from "@/types";

export const platformApi = {
  notifications: {
    list: (params?: { page?: number; unread?: boolean }) =>
      api.get<PaginatedResponse<Notification>>("/notifications", params),
    markRead: (id: string) => api.patch<ApiResponse<void>>(`/notifications/${id}/read`),
    markAllRead: () => api.post<ApiResponse<void>>("/notifications/read-all"),
  },

  workflows: {
    list: (params?: { page?: number; status?: string }) =>
      api.get<PaginatedResponse<Workflow>>("/workflows", params),
    get: (id: string) => api.get<ApiResponse<Workflow>>(`/workflows/${id}`),
    create: (data: Partial<Workflow>) => api.post<ApiResponse<Workflow>>("/workflows", data),
    run: (id: string) => api.post<ApiResponse<void>>(`/workflows/${id}/run`),
  },

  plugins: {
    list: (params?: { category?: string; installed?: boolean }) =>
      api.get<PaginatedResponse<Plugin>>("/marketplace", params),
    install: (id: string) => api.post<ApiResponse<void>>(`/marketplace/${id}/install`),
    uninstall: (id: string) => api.post<ApiResponse<void>>(`/marketplace/${id}/uninstall`),
  },

  audit: {
    list: (params?: { page?: number; action?: string; user?: string }) =>
      api.get<PaginatedResponse<AuditLog>>("/audit", params),
  },

  search: (query: string, types?: string[]) =>
    api.get<ApiResponse<SearchResult[]>>("/search", { q: query, types: types?.join(",") }),

  metrics: () => api.get<ApiResponse<Record<string, number>>>("/analytics/metrics"),
};
