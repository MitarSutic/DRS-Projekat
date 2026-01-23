import { useState } from "react";
import { login as loginApi } from "../api/authApi";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginApi(email, password);
      login(data);
      navigate("/");
    } catch {
      alert("Pogrešan email ili lozinka");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Prijava</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Lozinka" onChange={e => setPassword(e.target.value)} />
      <button>Login</button>
    </form>
  );
}
