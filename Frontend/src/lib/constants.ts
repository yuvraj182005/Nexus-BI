export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const APP_NAME = "NexusBI AI";
export const APP_TAGLINE = "One Intelligent Platform for Data, Analytics, AI & Business Decisions";

export const ROUTES = {
  home: "/",
  login: "/login",
  register: "/register",
  dashboard: "/dashboard",
  workspace: "/workspace",
  datasets: "/datasets",
  datasetUpload: "/datasets/upload",
  datasetProfiling: "/datasets/profiling",
  dataCleaning: "/datasets/cleaning",
  sqlStudio: "/sql-studio",
  analytics: "/analytics",
  forecasting: "/forecasting",
  insights: "/insights",
  dashboardBuilder: "/dashboard-builder",
  visualization: "/visualization",
  reports: "/reports",
  copilot: "/copilot",
  chat: "/chat",
  workflows: "/workflows",
  monitoring: "/monitoring",
  notifications: "/notifications",
  marketplace: "/marketplace",
  plugins: "/plugins",
  governance: "/governance",
  audit: "/audit",
  search: "/search",
  admin: "/admin",
  billing: "/billing",
  profile: "/profile",
  settings: "/settings",
  help: "/help",
  docs: "/docs",
} as const;

export const NAV_SECTIONS = [
  {
    title: "Overview",
    items: [
      { label: "Dashboard", href: ROUTES.dashboard, icon: "LayoutDashboard" },
      { label: "Workspace", href: ROUTES.workspace, icon: "Briefcase" },
      { label: "Search", href: ROUTES.search, icon: "Search" },
    ],
  },
  {
    title: "Data",
    items: [
      { label: "Datasets", href: ROUTES.datasets, icon: "Database" },
      { label: "Upload", href: ROUTES.datasetUpload, icon: "Upload" },
      { label: "Profiling", href: ROUTES.datasetProfiling, icon: "ScanSearch" },
      { label: "Data Cleaning", href: ROUTES.dataCleaning, icon: "Sparkles" },
      { label: "SQL Studio", href: ROUTES.sqlStudio, icon: "Terminal" },
    ],
  },
  {
    title: "Analytics",
    items: [
      { label: "Analytics Studio", href: ROUTES.analytics, icon: "BarChart3" },
      { label: "Forecasting", href: ROUTES.forecasting, icon: "TrendingUp" },
      { label: "Business Insights", href: ROUTES.insights, icon: "Lightbulb" },
      { label: "Visualization", href: ROUTES.visualization, icon: "PieChart" },
      { label: "Reports", href: ROUTES.reports, icon: "FileText" },
    ],
  },
  {
    title: "Build",
    items: [
      { label: "Dashboard Builder", href: ROUTES.dashboardBuilder, icon: "LayoutGrid" },
      { label: "Workflows", href: ROUTES.workflows, icon: "GitBranch" },
      { label: "Real-time Monitor", href: ROUTES.monitoring, icon: "Activity" },
    ],
  },
  {
    title: "AI",
    items: [
      { label: "AI Copilot", href: ROUTES.copilot, icon: "Bot" },
      { label: "Chat with Data", href: ROUTES.chat, icon: "MessageSquare" },
    ],
  },
  {
    title: "Platform",
    items: [
      { label: "Marketplace", href: ROUTES.marketplace, icon: "Store" },
      { label: "Plugins", href: ROUTES.plugins, icon: "Puzzle" },
      { label: "Governance", href: ROUTES.governance, icon: "Shield" },
      { label: "Audit Center", href: ROUTES.audit, icon: "ClipboardList" },
    ],
  },
  {
    title: "Account",
    items: [
      { label: "Admin Portal", href: ROUTES.admin, icon: "Settings2" },
      { label: "Billing", href: ROUTES.billing, icon: "CreditCard" },
      { label: "Notifications", href: ROUTES.notifications, icon: "Bell" },
      { label: "Settings", href: ROUTES.settings, icon: "Settings" },
      { label: "Help Center", href: ROUTES.help, icon: "HelpCircle" },
      { label: "Documentation", href: ROUTES.docs, icon: "BookOpen" },
    ],
  },
] as const;
