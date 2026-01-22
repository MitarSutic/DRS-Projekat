import { useState, useEffect } from "react";

export default function ProfilePage() {
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const [file, setFile] = useState(null);

  // Učitavanje podataka korisnika
  const fetchUser = () => {
    if (!token) {
      alert("Niste prijavljeni!");
      setLoading(false);
      return;
    }

    setLoading(true);

    fetch("http://localhost:5000/users/me", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.msg || "Greška pri učitavanju korisnika");
        }
        return res.json();
      })
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        alert(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!token) return alert("Niste prijavljeni!");

    const formData = new FormData();
    for (const key in user) {
      formData.append(key, user[key]);
    }
    if (file) formData.append("profile_picture", file);

    fetch("http://localhost:5000/users/me", {
      method: "PATCH",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
      body: formData,
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.msg || "Greška pri update-u");
        }
        alert(data.msg || "Podaci uspešno izmenjeni!");
        fetchUser(); // osveži podatke
      })
      .catch((err) => {
        console.error(err);
        alert(err.message);
      });
  };

  if (loading) return <p>Učitavanje...</p>;

  return (
    <div>
      <h1>Moj profil</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Ime:</label>
          <input name="ime" value={user.ime || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Prezime:</label>
          <input
            name="prezime"
            value={user.prezime || ""}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input name="email" value={user.email || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Pol:</label>
          <input name="pol" value={user.pol || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Država:</label>
          <input name="drzava" value={user.drzava || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Ulica:</label>
          <input name="ulica" value={user.ulica || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Broj:</label>
          <input name="broj" value={user.broj || ""} onChange={handleChange} />
        </div>
        <div>
          <label>Profilna slika:</label>
          <input type="file" onChange={handleFileChange} />
        </div>
        <button type="submit">Sačuvaj promene</button>
      </form>
    </div>
  );
}
