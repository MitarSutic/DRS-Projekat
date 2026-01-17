import React, { useState } from "react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // 👇 Custom validacija
    if (!email || !password) {
      alert("Email i lozinka su obavezni!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Login uspešan!");
        localStorage.setItem("token", data.access_token);
          // Provera role
        const decoded = parseJwt(data.access_token); // funkcija koja dekoduje JWT
        if (decoded.role === "ADMINISTRATOR") {
          window.location.href = "/admin"; // preusmeri na admin stranicu
        } 
        else {
          window.location.href = "/profile"; // ili običan korisnik
        }
      }
        
       else {
        alert(data.msg);
      }
    } catch (error) {
      alert("Došlo je do greške: " + error.message);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br /><br />
        <input
          type="password"
          placeholder="Lozinka"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br /><br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

export default Login;