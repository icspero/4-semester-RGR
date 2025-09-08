import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const data = new URLSearchParams();
      data.append("username", username);
      data.append("password", password);

      const response = await axios.post("http://127.0.0.1:8000/login/", data, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token);
      navigate("/home");
    } catch (err) {
      if (err.response) {
        if (err.response.status === 401) {
          setError("Неверный логин или пароль");
        } else if (err.response.status === 422) {
          setError("Ошибка формата данных. Проверьте ввод.");
        } else {
          setError("Ошибка сервера. Попробуйте позже.");
        }
      } else {
        setError("Сервер недоступен");
      }
    }
  };

  const goToRegister = () => {
    navigate("/register"); // редирект на страницу регистрации
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
      <h2>Вход в систему</h2>
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "10px" }}>
          <label>Логин:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <label>Пароль:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: "20px" }}>
          <button type="submit" style={{ padding: "10px 20px" }}>
            Войти
          </button>
          <button type="button" onClick={goToRegister} style={{ padding: "10px 20px" }}>
            Регистрация
          </button>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;