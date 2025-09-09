import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function HomePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    if (token) {
      axios
        .get("http://127.0.0.1:8000/me", {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => setUser(res.data))
        .catch(err => console.error("Ошибка при получении пользователя", err));
    }
  }, [token]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    navigate("/login");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Главная страница</h1>

      {user && (
        <>
          <h2>Добро пожаловать, {user.first_name} {user.last_name}!</h2>
          <p>Ваша роль: {user.role?.name}</p>
        </>
      )}

      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button onClick={() => navigate("/my-patients")}>
          Мои пациенты
        </button>
        <button onClick={() => navigate("/add-patient")}>
          Добавить пациента
        </button>
        <button onClick={() => navigate("/add-card")}>
          Создать медкарту
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <button
          onClick={handleLogout}
          style={{ marginTop: "20px", display: "flex", gap: "10px" }}
        >
          Выйти
        </button>
      </div>
    </div>
  );
}

export default HomePage;