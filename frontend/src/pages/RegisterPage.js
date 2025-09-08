import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const RegisterPage = () => {
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [middleName, setMiddleName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [roleId, setRoleId] = useState(""); // выбранная роль
  const [roles, setRoles] = useState([]);   // список ролей с сервера
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Загружаем роли с сервера при монтировании компонента
    axios.get("http://127.0.0.1:8000/roles/")
      .then(res => setRoles(res.data))
      .catch(err => console.error("Не удалось загрузить роли", err));
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }

    if (!roleId) {
      setError("Выберите роль");
      return;
    }

    try {
      const data = {
        last_name: lastName,
        first_name: firstName,
        middle_name: middleName,
        phone_number: phoneNumber,
        login: login,
        password: password,
        role_id: roleId
      };

      await axios.post("http://127.0.0.1:8000/register/", data, {
        headers: { "Content-Type": "application/json" },
      });

      setSuccess("Регистрация успешна! Теперь можете войти!");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      if (err.response) {
        if (err.response.status === 400) {
          setError("Пользователь с таким логином уже существует");
        } else {
          setError("Ошибка сервера. Попробуйте позже.");
        }
      } else {
        setError("Сервер недоступен");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto" }}>
      <h2>Регистрация сотрудника</h2>
      <form onSubmit={handleRegister}>
        <input type="text" placeholder="Фамилия" value={lastName} onChange={e => setLastName(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="text" placeholder="Имя" value={firstName} onChange={e => setFirstName(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="text" placeholder="Отчество" value={middleName} onChange={e => setMiddleName(e.target.value)} style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="text" placeholder="Телефон" value={phoneNumber} onChange={e => setPhoneNumber(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="text" placeholder="Логин" value={login} onChange={e => setLogin(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />
        <input type="password" placeholder="Повторите пароль" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }} />

        {/* Выпадающий список для роли */}
        <select value={roleId} onChange={e => setRoleId(e.target.value)} required style={{ width: "100%", padding: "8px", marginBottom: "10px" }}>
          <option value="">Выберите роль</option>
          {roles.map(role => (
            <option key={role.role_id} value={role.role_id}>{role.name}</option>
          ))}
        </select>

        {error && <p style={{ color: "red" }}>{error}</p>}
        {success && <p style={{ color: "green" }}>{success}</p>}
        <button type="submit" style={{ padding: "10px 20px" }}>Зарегистрировать</button>
      </form>
    </div>
  );
};

export default RegisterPage;
