import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const RequireAuth = ({ children, roles }) => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" />;

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" />;
  }

  return children;
};

export default RequireAuth;
