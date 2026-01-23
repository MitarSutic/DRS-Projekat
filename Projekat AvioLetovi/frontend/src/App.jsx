import { Routes, Route, Link } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import Admin from "./pages/Admin";
//import Flights from "./pages/Flights";
import RequireAuth from "./auth/RequireAuth";
import { useAuth } from "./auth/AuthContext";
import { ROLES } from "./utils/roles";
import './App.css'

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav>
      {!user && (
        <>
          <Link to="/login">Login</Link> |{" "}
          <Link to="/register">Register</Link>
        </>
      )}

      {user && (
        <>
          <Link to="/">Letovi</Link> |{" "}
          <Link to="/profile">Profil</Link> |{" "}
          {user.role === ROLES.ADMIN && (
            <>
              {" | "}
              <Link to="/admin">Admin</Link>
            </>
          )}
          {" | "}
          <button onClick={logout}>Logout</button>
        </>
      )}
    </nav>
  );
}

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />



        <Route
          path="/admin"
          element={
            <RequireAuth roles={["ADMIN"]}>
              <Admin />
            </RequireAuth>
          }
        />
      </Routes>
    </>
  );
}


export default App;
