import { useEffect, useState } from "react";
import { getAllUsers, changeUserRole } from "../api/usersApi";

export default function Admin() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await getAllUsers();
      setUsers(data || []);
    } catch (err) {
      alert("Greška pri učitavanju korisnika");
    } finally {
      setLoading(false);
    }
  };

  const makeManager = async (userId) => {
    try {
      await changeUserRole(userId, "MENADZER");
      alert("Uloga promijenjena");
      fetchUsers();
    } catch {
      alert("Greška pri promeni uloge");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  if (loading) return <p>Učitavanje...</p>;

  return (
    <div>
      <h1>Admin panel</h1>

      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>Email</th>
            <th>Uloga</th>
            <th>Akcija</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.email}</td>
              <td>{u.uloga}</td>
              <td>
                {u.uloga === "KORISNIK" && (
                  <button onClick={() => makeManager(u.id)}>
                    Dodeli MENADŽERA
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
