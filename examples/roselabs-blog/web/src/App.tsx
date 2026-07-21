import { createBrowserRouter } from "react-router-dom";

import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { AcceptInvitePage } from "./pages/AcceptInvitePage";
import { AdminAuthorsPage } from "./pages/AdminAuthorsPage";
import { DashboardPage } from "./pages/DashboardPage";
import { EditorPage } from "./pages/EditorPage";
import { LoginPage } from "./pages/LoginPage";
import { ModerationPage } from "./pages/ModerationPage";
import { PostDetailPage } from "./pages/PostDetailPage";
import { PostListPage } from "./pages/PostListPage";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <PostListPage /> },
      { path: "/posts/:slug", element: <PostDetailPage /> },
      { path: "/login", element: <LoginPage /> },
      { path: "/accept-invite", element: <AcceptInvitePage /> },
      {
        element: <ProtectedRoute />,
        children: [
          { path: "/admin", element: <DashboardPage /> },
          { path: "/admin/moderation", element: <ModerationPage /> },
          { path: "/admin/authors", element: <AdminAuthorsPage /> },
          { path: "/admin/new", element: <EditorPage /> },
          { path: "/admin/posts/:id", element: <EditorPage /> },
        ],
      },
    ],
  },
]);
