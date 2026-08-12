export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: "admin" | "analyst" | "viewer" | "developer";
  organization: string;
  createdAt: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  organization?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface Dataset {
  id: string;
  name: string;
  description?: string;
  type: "csv" | "json" | "parquet" | "sql" | "api";
  size: number;
  rows: number;
  columns: number;
  status: "active" | "processing" | "error" | "archived";
  quality: number;
  lastUpdated: string;
  createdBy: string;
  tags: string[];
}

export interface Dashboard {
  id: string;
  name: string;
  description?: string;
  thumbnail?: string;
  widgets: number;
  views: number;
  lastModified: string;
  createdBy: string;
  isPublic: boolean;
  tags: string[];
}

export interface Metric {
  label: string;
  value: number | string;
  change?: number;
  changeType?: "increase" | "decrease" | "neutral";
  prefix?: string;
  suffix?: string;
  icon?: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: "info" | "success" | "warning" | "error";
  read: boolean;
  createdAt: string;
  actionUrl?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  status: "active" | "paused" | "draft" | "error";
  triggers: number;
  lastRun?: string;
  nextRun?: string;
  successRate: number;
}

export interface Plugin {
  id: string;
  name: string;
  description: string;
  version: string;
  author: string;
  category: string;
  installed: boolean;
  rating: number;
  downloads: number;
}

export interface AuditLog {
  id: string;
  action: string;
  resource: string;
  user: string;
  timestamp: string;
  ip: string;
  status: "success" | "failure";
  details?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface ForecastResult {
  id: string;
  metric: string;
  period: string;
  confidence: number;
  predictions: { date: string; value: number; lower: number; upper: number }[];
}

export interface SearchResult {
  id: string;
  type: "dataset" | "dashboard" | "report" | "workflow" | "user";
  title: string;
  description?: string;
  url: string;
  relevance: number;
}

export interface BillingPlan {
  id: string;
  name: string;
  price: number;
  interval: "month" | "year";
  features: string[];
  limits: Record<string, number>;
}

export interface ActivityItem {
  id: string;
  type: string;
  title: string;
  description: string;
  user: string;
  timestamp: string;
  icon?: string;
}
