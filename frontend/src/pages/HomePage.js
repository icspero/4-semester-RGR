import React, { useState, useEffect } from "react";
import axios from "axios";

function HomePage() {
  const [user, setUser] = useState(null);
  const [patients, setPatients] = useState([]);
  const [showPatients, setShowPatients] = useState(false);
  const [showAddPatient, setShowAddPatient] = useState(false);
  const [showAddCard, setShowAddCard] = useState(false);

  const [newPatient, setNewPatient] = useState({
    full_name: "",
    phone_number: "",
    is_patient: true
  });

  const [newCard, setNewCard] = useState({
    patient_id: "",
    diagnosis: "",
    treatment_plan: ""
  });

  const token = localStorage.getItem("access_token");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/me", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => setUser(res.data))
      .catch(err => console.error("Ошибка при получении пользователя", err));
  }, [token]);

  const fetchPatients = () => {
    axios
      .get("http://127.0.0.1:8000/my-patients", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => setPatients(res.data))
      .catch(err => console.error("Ошибка при получении пациентов", err));
  };

  const handlePatientChange = e => {
    const { name, value } = e.target;
    setNewPatient(prev => ({ ...prev, [name]: value }));
  };

  const handleAddPatient = () => {
    axios
      .post("http://127.0.0.1:8000/patients/", newPatient, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        alert("Пациент добавлен!");
        setShowAddPatient(false);
      })
      .catch(err => console.error("Ошибка добавления пациента", err));
  };

  const handleCardChange = e => {
    const { name, value } = e.target;
    setNewCard(prev => ({ ...prev, [name]: value }));
  };

  const handleAddCard = () => {
    axios
      .post("http://127.0.0.1:8000/medicalcards/", newCard, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        alert("Медкарта создана!");
        setShowAddCard(false);
      })
      .catch(err => console.error("Ошибка создания карты", err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Главная страница</h1>
      {user && (
        <>
          <h2>Добро пожаловать, {user.first_name} {user.middle_name}!</h2>
          <p>Ваша роль: {user.role?.name}</p>
        </>
      )}

      <div style={{ marginTop: "20px" }}>
        <button onClick={() => { setShowPatients(!showPatients); if (!showPatients) fetchPatients(); }}>
          {showPatients ? "Скрыть пациентов" : "Мои пациенты"}
        </button>
        <button onClick={() => setShowAddPatient(!showAddPatient)}>
          {showAddPatient ? "Отмена" : "Добавить пациента"}
        </button>
        <button onClick={() => setShowAddCard(!showAddCard)}>
          {showAddCard ? "Отмена" : "Создать медкарту"}
        </button>
      </div>

      {showPatients && (
        <div style={{ marginTop: "20px" }}>
          <h3>Мои пациенты</h3>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ФИО</th>
                <th>Телефон</th>
                <th>Дата регистрации</th>
              </tr>
            </thead>
            <tbody>
              {patients.map(p => (
                <tr key={p.visitor_id}>
                  <td>{p.full_name}</td>
                  <td>{p.phone_number}</td>
                  <td>{new Date(p.date_registration).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showAddPatient && (
        <div style={{ marginTop: "20px" }}>
          <h3>Добавить пациента</h3>
          <input
            type="text"
            name="full_name"
            placeholder="ФИО"
            value={newPatient.full_name}
            onChange={handlePatientChange}
          />
          <input
            type="text"
            name="phone_number"
            placeholder="Телефон"
            value={newPatient.phone_number}
            onChange={handlePatientChange}
          />
          <button onClick={handleAddPatient}>Сохранить</button>
        </div>
      )}

      {showAddCard && (
        <div style={{ marginTop: "20px" }}>
          <h3>Создать медкарту</h3>
          <select
            name="patient_id"
            value={newCard.patient_id}
            onChange={handleCardChange}
          >
            <option value="">Выберите пациента</option>
            {patients.map(p => (
              <option key={p.visitor_id} value={p.visitor_id}>
                {p.full_name}
              </option>
            ))}
          </select>
          <input
            type="text"
            name="diagnosis"
            placeholder="Диагноз"
            value={newCard.diagnosis}
            onChange={handleCardChange}
          />
          <input
            type="text"
            name="treatment_plan"
            placeholder="План лечения"
            value={newCard.treatment_plan}
            onChange={handleCardChange}
          />
          <button onClick={handleAddCard}>Сохранить</button>
        </div>
      )}
    </div>
  );
}

export default HomePage;