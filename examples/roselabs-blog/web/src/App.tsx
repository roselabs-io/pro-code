import { createBrowserRouter } from "react-router-dom";

import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
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
      {
        element: <ProtectedRoute />,
        children: [
          { path: "/admin", element: <DashboardPage /> },
          { path: "/admin/moderation", element: <ModerationPage /> },
          { path: "/admin/new", element: <EditorPage /> },
          { path: "/admin/posts/:id", element: <EditorPage /> },
        ],
      },
    ],
  },
]);
