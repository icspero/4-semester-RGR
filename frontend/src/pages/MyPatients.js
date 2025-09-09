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
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        const doctorId = res.data.staff_id;
        return axios.get(
          `http://127.0.0.1:8000/doctorpatient/by-doctor/${doctorId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      })
      .then(res => {
        setPatients(res.data);
        setLoading(false);
      })
      .catch(err => {
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

      {loading && <div style={{ marginTop: "10px" }}>Загрузка пациентов...</div>}
      {error && <div style={{ marginTop: "10px", color: "red" }}>{error}</div>}
      {!loading && !error && patients.length === 0 && (
        <div style={{ marginTop: "10px" }}>Пациентов пока нет</div>
      )}

      {!loading && !error && patients.length > 0 && (
        <>
          <h2 style={{ marginTop: "10px" }}>Мои пациенты</h2>
          <table
            border="1"
            cellPadding="8"
            style={{ borderCollapse: "collapse", width: "100%", marginTop: "10px" }}
          >
            <thead style={{ backgroundColor: "#f0f0f0" }}>
              <tr>
                <th>Имя пациента</th>
                <th>Телефон</th>
                <th>Диагноз</th>
                <th>План лечения</th>
              </tr>
            </thead>
            <tbody>
              {patients.map((dp, index) => {
                const patient = dp.patient;
                return (
                  <tr key={index}>
                    <td>{patient.full_name}</td>
                    <td>{patient.phone_number || "-"}</td>
                    <td>{patient.latest_card?.diagnosis || "-"}</td>
                    <td>{patient.latest_card?.treatment_plan || "-"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default MyPatients;