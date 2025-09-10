import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function MyPatients() {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
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
      .get("http://127.0.0.1:8000/me/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        const doctorId = res.data.staff_id;
        return axios.get(
          `http://127.0.0.1:8000/doctorpatient/by-doctor/${doctorId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      })
      .then((res) => {
        setPatients(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Ошибка при получении пациентов", err);
        setError("Не удалось загрузить пациентов");
        setLoading(false);
      });
  }, [token]);

  return (
    <div style={{ padding: "20px" }}>
      <button
        onClick={() => navigate("/home")}
        style={{ marginBottom: "16px", padding: "8px 16px", cursor: "pointer" }}
      >
        Назад на главную
      </button>

      {loading && <div>Загрузка пациентов...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      {!loading && !error && patients.length === 0 && (
        <div>Пациентов пока нет</div>
      )}

      {!loading && !error && patients.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {patients.map((dp, index) => {
            const patient = dp.patient;
            return (
              <button
                key={index}
                onClick={() => navigate(`/patients/${patient.visitor_id}`)}
                style={{
                  padding: "12px",
                  textAlign: "left",
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  cursor: "pointer",
                  backgroundColor: "#f9f9f9",
                }}
              >
                {patient.full_name}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default MyPatients;