import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function AddPatient() {
  const [patient, setPatient] = useState({
    full_name: "",
    phone_number: "",
    is_patient: true
  });

  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setPatient({
      ...patient,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/patients/", patient, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert("Пациент успешно добавлен!");
      setPatient({ full_name: "", phone_number: "", is_patient: true });
    } catch (err) {
      console.error("Ошибка добавления пациента:", err);
      alert("Ошибка при добавлении пациента");
    }
  };

  return (
    <div style={{ marginTop: "20px", padding: "20px" }}>
      <h2>Добавить пациента</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            name="full_name"
            placeholder="ФИО"
            value={patient.full_name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <input
            type="text"
            name="phone_number"
            placeholder="Телефон"
            value={patient.phone_number}
            onChange={handleChange}
            required
          />
        </div>
        <div style={{ marginTop: "10px" }}>
          <button type="submit">Сохранить</button>
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

export default AddPatient;
