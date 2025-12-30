import { Routes, Route, Link } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";

import './App.css'

function App() {
  return (
    <div>
      <nav>
        <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}


export default App
