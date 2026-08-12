import { api } from "./client";
import type { ApiResponse, ChatMessage, ForecastResult, PaginatedResponse } from "@/types";

export const aiApi = {
  chat: (message: string, context?: Record<string, unknown>) =>
    api.post<ApiResponse<ChatMessage>>("/chat", { message, context }),

  chatHistory: (params?: { page?: number; pageSize?: number }) =>
    api.get<PaginatedResponse<ChatMessage>>("/chat/history", params),

  copilot: (prompt: string, context?: Record<string, unknown>) =>
    api.post<ApiResponse<ChatMessage>>("/copilot", { prompt, context }),

  generateSql: (naturalLanguage: string, schema?: string) =>
    api.post<ApiResponse<{ sql: string; explanation: string }>>("/sql/generate", {
      query: naturalLanguage,
      schema,
    }),

  executeSql: (sql: string, datasetId?: string) =>
    api.post<ApiResponse<{ columns: string[]; rows: Record<string, unknown>[]; executionTimeMs: number }>>("/sql/execute", {
      sql,
      datasetId,
    }),

  forecast: (datasetId: string, config: Record<string, unknown>) =>
    api.post<ApiResponse<ForecastResult>>("/forecasting/generate", { datasetId, ...config }),

  insights: (datasetId: string) =>
    api.post<ApiResponse<{ insights: string[] }>>("/insights/generate", { datasetId }),
};
