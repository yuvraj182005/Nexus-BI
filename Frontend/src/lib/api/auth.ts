import { api } from "./client";
import type {
  ApiResponse,
  AuthTokens,
  LoginRequest,
  RegisterRequest,
  User,
} from "@/types";

export const authApi = {
  login: (data: LoginRequest) =>
    api.post<ApiResponse<AuthTokens & { user: User }>>("/auth/login", data),

  register: (data: RegisterRequest) =>
    api.post<ApiResponse<AuthTokens & { user: User }>>("/auth/register", data),

  logout: () => api.post<ApiResponse<void>>("/auth/logout"),

  refresh: (refreshToken: string) =>
    api.post<ApiResponse<AuthTokens>>("/auth/refresh", { refreshToken }),

  me: () => api.get<ApiResponse<User>>("/identity/me"),
};
