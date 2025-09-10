import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function AddCard() {
  const [patients, setPatients] = useState([]);
  const [newCard, setNewCard] = useState({
    patient_id: "",
    diagnosis: "",
    treatment_plan: ""
  });
  const [user, setUser] = useState(null);

  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) return;

    axios.get("http://127.0.0.1:8000/me/", {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then(res => setUser(res.data))
    .catch(err => console.error("Ошибка при получении пользователя", err));

    axios.get("http://127.0.0.1:8000/patients/", {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then(res => setPatients(res.data))
    .catch(err => console.error("Ошибка при получении пациентов", err));
  }, [token]);

  const handleChange = e => {
    const { name, value } = e.target;
    setNewCard(prev => ({ ...prev, [name]: value }));
  };

  const handleAddCard = async e => {
    e.preventDefault();

    if (!token || !user) {
      alert("Вы не авторизованы!");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/cards", newCard, {
        headers: { Authorization: `Bearer ${token}` },
      });

      await axios.post(
        "http://127.0.0.1:8000/doctorpatient/",
        {
          doctor_id: parseInt(user.staff_id),     
          patient_id: parseInt(newCard.patient_id)   
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      alert("Медкарта создана и пациент привязан к врачу!");
      setNewCard({ patient_id: "", diagnosis: "", treatment_plan: "" });
      navigate("/home");
    } catch (err) {
      console.error("Ошибка создания медкарты:", err);
      alert("Ошибка при создании медкарты, у вас уже есть этот пациент!");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Создать медкарту</h2>
      {user && <p>Врач: {user.first_name} {user.last_name}</p>}
      <form onSubmit={handleAddCard}>
        <div>
          <select
            name="patient_id"
            value={newCard.patient_id}
            onChange={handleChange}
            required
          >
            <option value="">Выберите пациента</option>
            {patients.map(p => (
              <option key={p.visitor_id} value={p.visitor_id}>
                {p.full_name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <input
            type="text"
            name="diagnosis"
            placeholder="Диагноз"
            value={newCard.diagnosis}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <input
            type="text"
            name="treatment_plan"
            placeholder="План лечения"
            value={newCard.treatment_plan}
            onChange={handleChange}
            required
          />
        </div>
        <div style={{ marginTop: "10px" }}>
          <button type="submit">Создать медкарту</button>
          <button
            type="button"
            onClick={() => navigate("/home")}
            style={{ marginLeft: "10px" }}
          >
            Назад на главную
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddCard;