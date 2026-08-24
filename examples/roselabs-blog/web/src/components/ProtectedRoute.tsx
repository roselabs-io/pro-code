import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../auth";

export function ProtectedRoute() {
  const { isAuthed } = useAuth();
  return isAuthed ? <Outlet /> : <Navigate to="/login" replace />;
}
