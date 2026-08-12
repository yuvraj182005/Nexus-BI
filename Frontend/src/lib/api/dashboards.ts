import { api } from "./client";
import type { ApiResponse, Dashboard, PaginatedResponse } from "@/types";

export const dashboardsApi = {
  list: (params?: { page?: number; pageSize?: number; search?: string }) =>
    api.get<PaginatedResponse<Dashboard>>("/dashboards", params),

  get: (id: string) => api.get<ApiResponse<Dashboard>>(`/dashboards/${id}`),

  create: (data: Partial<Dashboard>) =>
    api.post<ApiResponse<Dashboard>>("/dashboards", data),

  update: (id: string, data: Partial<Dashboard>) =>
    api.put<ApiResponse<Dashboard>>(`/dashboards/${id}`, data),

  delete: (id: string) => api.delete<ApiResponse<void>>(`/dashboards/${id}`),

  duplicate: (id: string) =>
    api.post<ApiResponse<Dashboard>>(`/dashboards/${id}/duplicate`),
};
