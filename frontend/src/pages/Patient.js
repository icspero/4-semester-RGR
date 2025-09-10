import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function Patient() {
  const { id } = useParams(); // id из URL
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("access_token");

  useEffect(() => {
    if (!token) {
      setError("Нет токена");
      setLoading(false);
      return;
    }

    axios
      .get(`http://127.0.0.1:8000/patients/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        setPatient(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Ошибка при получении пациента", err);
        setError("Не удалось загрузить данные пациента");
        setLoading(false);
      });
  }, [id, token]);

  return (
    <div style={{ padding: "20px" }}>
      <button
        onClick={() => navigate("/my-patients")}
        style={{ marginBottom: "16px", padding: "8px 16px", cursor: "pointer" }}
      >
        Назад к пациентам
      </button>

      {loading && <div>Загрузка...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      {patient && (
        <div style={{ marginTop: "10px" }}>
          <h2>{patient.full_name}</h2>
          <p><b>Телефон:</b> {patient.phone_number || "-"}</p>
          <p><b>Диагноз:</b> {patient.latest_card?.diagnosis || "-"}</p>
          <p><b>План лечения:</b> {patient.latest_card?.treatment_plan || "-"}</p>
        </div>
      )}
    </div>
  );
}

export default Patient;