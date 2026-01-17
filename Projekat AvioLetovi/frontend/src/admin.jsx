import { useState, useEffect } from "react";

export default function AdminPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");

  // Funkcija za učitavanje svih korisnika sa backend-a
  const fetchUsers = () => {
    if (!token) {
      alert("Niste prijavljeni!");
      setLoading(false);
      return;
    }

    setLoading(true);

    fetch("http://localhost:5000/admin/users", {
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
        setUsers(data || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        alert(err.message);
        setLoading(false);
      });
  };

  // Funkcija za dodelu uloge MENADŽER
  const makeManager = (userId) => {
    if (!token) {
      alert("Niste prijavljeni!");
      return;
    }

    fetch(`http://localhost:5000/admin/users/${userId}/role`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ uloga: "MENADZER" }),
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) {
          alert(data.msg || "Greška pri promeni uloge");
          return;
        }
        alert(data.msg || "Uloga promenjena!");
        // Osveži listu korisnika iz baze
        fetchUsers();
      })
      .catch((err) => {
        console.error(err);
        alert("Greška pri promeni uloge");
      });
  };

  // Učitaj korisnike pri mount-u komponente
  useEffect(() => {
    fetchUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (loading) return <p>Učitavanje...</p>;

  return (
    <div>
      <h1>Admin panel</h1>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ime</th>
            <th>Prezime</th>
            <th>Email</th>
            <th>Uloga</th>
            <th>Akcija</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.ime}</td>
              <td>{u.prezime}</td>
              <td>{u.email}</td>
              <td>{u.uloga}</td>
              <td>
                {u.uloga === "KORISNIK" && (
                  <button onClick={() => makeManager(u.id)}>
                    Dodeli ulogu MENADŽER
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
