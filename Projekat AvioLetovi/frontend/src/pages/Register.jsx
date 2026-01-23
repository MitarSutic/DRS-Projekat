import { useState } from "react";
import { register as registerApi } from "../api/authApi";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    ime: "",
    prezime: "",
    email: "",
    lozinka: "",
    datumRodjenja: "",
    pol: "",
    drzava: "",
    ulica: "",
    broj: "",
    stanje: 0,
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await registerApi(form);
      alert("Registracija uspešna! Možete se prijaviti.");
      navigate("/login");
    } catch (err) {
      alert("Greška pri registraciji");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Registracija</h2>

      <input name="ime" placeholder="Ime" onChange={handleChange} required />
      <input name="prezime" placeholder="Prezime" onChange={handleChange} required />
      <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
      <input name="lozinka" type="password" placeholder="Lozinka" onChange={handleChange} required />

      <label>Datum rođenja</label>
      <input name="datumRodjenja" type="date" onChange={handleChange} required />

      <select name="pol" onChange={handleChange} required>
        <option value="">Pol</option>
        <option value="M">Muški</option>
        <option value="Z">Ženski</option>
      </select>

      <input name="drzava" placeholder="Država" onChange={handleChange} required />
      <input name="ulica" placeholder="Ulica" onChange={handleChange} required />
      <input name="broj" placeholder="Broj" onChange={handleChange} required />

      <input
        name="stanje"
        type="number"
        placeholder="Početno stanje"
        onChange={handleChange}
        min="0"
      />

      <button type="submit">Registruj se</button>
    </form>
  );
}
