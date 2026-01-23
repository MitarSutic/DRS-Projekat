import api from "./axios";

export const getAllUsers = async () => {
  const res = await api.get("/admin/users");
  return res.data;
};

export const changeUserRole = async (userId, role) => {
  const res = await api.patch(`/admin/users/${userId}/role`, {
    uloga: role,
  });
  return res.data;
};
