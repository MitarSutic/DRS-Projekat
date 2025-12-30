import React, { useState } from "react";

function Register() {
  const [formData, setFormData] = useState({
    ime: "",
    prezime: "",
    email: "",
    password: "",
    datumRodjenja: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:5000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    if (response.ok) {
      alert("Registracija uspešna!");
    } else {
      alert("Greška: " + data.msg);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="ime" placeholder="Ime" value={formData.ime} onChange={handleChange} required /><br /><br />
        <input type="text" name="prezime" placeholder="Prezime" value={formData.prezime} onChange={handleChange} required /><br /><br />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required /><br /><br />
        <input type="password" name="password" placeholder="Lozinka" value={formData.password} onChange={handleChange} required /><br /><br />
        <input type="date" name="datumRodjenja" value={formData.datumRodjenja || ""} onChange={handleChange} required /><br /><br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;