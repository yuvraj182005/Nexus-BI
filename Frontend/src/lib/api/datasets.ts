import { api } from "./client";
import type { ApiResponse, Dataset, PaginatedResponse } from "@/types";

export const datasetsApi = {
  list: (params?: { page?: number; pageSize?: number; search?: string; status?: string }) =>
    api.get<PaginatedResponse<Dataset>>("/datasets", params),

  get: (id: string) => api.get<ApiResponse<Dataset>>(`/datasets/${id}`),

  create: (data: Partial<Dataset>) =>
    api.post<ApiResponse<Dataset>>("/datasets", data),

  update: (id: string, data: Partial<Dataset>) =>
    api.put<ApiResponse<Dataset>>(`/datasets/${id}`, data),

  delete: (id: string) => api.delete<ApiResponse<void>>(`/datasets/${id}`),

  upload: (file: File, metadata?: Record<string, string>) => {
    const formData = new FormData();
    formData.append("file", file);
    if (metadata) {
      Object.entries(metadata).forEach(([key, value]) => {
        formData.append(key, value);
      });
    }
    return api.upload<ApiResponse<Dataset>>("/datasets/upload", formData);
  },

  profile: (id: string) =>
    api.post<ApiResponse<Record<string, unknown>>>(`/profiling/${id}`),

  clean: (id: string, rules: Record<string, unknown>) =>
    api.post<ApiResponse<Dataset>>(`/preprocessing/clean`, { datasetId: id, rules }),
};
