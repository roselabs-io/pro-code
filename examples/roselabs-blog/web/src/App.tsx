import { createBrowserRouter } from "react-router-dom";

import { Layout } from "./components/Layout";
import { PostDetailPage } from "./pages/PostDetailPage";
import { PostListPage } from "./pages/PostListPage";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <PostListPage /> },
      { path: "/posts/:slug", element: <PostDetailPage /> },
    ],
  },
]);
