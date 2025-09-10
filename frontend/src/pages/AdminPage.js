import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function AdminPage() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const checkRole = useCallback(async () => {
    if (!token) {
      navigate("/login");
      return false;
    }

    try {
      const response = await axios.get("http://localhost:8000/me/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data.role?.name === "Doctor") {
        alert("У вас нет доступа к этой странице");
        navigate("/home");
        return false;
      }
      return true;
    } catch (err) {
      console.error("Ошибка при проверке роли:", err);
      navigate("/login");
      return false;
    }
  }, [token, navigate]);

  const fetchLogs = useCallback(
    async (currentPage) => {
      setLoading(true);
      try {
        const response = await axios.get(
          `http://localhost:8000/accesslog/?page=${currentPage}&size=5`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log("Логи с сервера:", response.data);
        setLogs(response.data.logs);
        setTotalPages(response.data.total_pages);
      } catch (err) {
        console.error("Ошибка при загрузке логов:", err);
      }
      setLoading(false);
    },
    [token]
  );

  useEffect(() => {
    const init = async () => {
      const allowed = await checkRole();
      if (allowed) {
        fetchLogs(page);
      }
    };
    init();
  }, [checkRole, fetchLogs, page]);

  const handlePrev = () => {
    if (page > 1) {
      const newPage = page - 1;
      setPage(newPage);
      fetchLogs(newPage);
    }
  };

  const handleNext = () => {
    if (page < totalPages) {
      const newPage = page + 1;
      setPage(newPage);
      fetchLogs(newPage);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Журнал доступа к медицинским картам</h2>
      <button onClick={() => navigate("/home")} style={{ marginBottom: "20px" }}>
        Назад на главную
      </button>

      {loading ? (
        <p>Загрузка данных...</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #333" }}>
              <th style={{ padding: "8px" }}>Врач</th>
              <th style={{ padding: "8px" }}>Медкарта (ID)</th>
              <th style={{ padding: "8px" }}>Дата и время просмотра</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan="3" style={{ padding: "8px", textAlign: "center" }}>
                  Нет данных
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.log_id} style={{ borderBottom: "1px solid #ccc" }}>
                  <td style={{ padding: "8px" }}>
                    {log.doctor_name || "Неизвестный врач"}
                  </td>
                  <td style={{ padding: "8px" }}>{log.card_id}</td>
                  <td style={{ padding: "8px" }}>
                    {new Date(log.access_time).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button onClick={handlePrev} disabled={page === 1}>
          Назад
        </button>
        <span>
          {page} / {totalPages}
        </span>
        <button onClick={handleNext} disabled={page === totalPages}>
          Вперед
        </button>
      </div>
    </div>
  );
}

export default AdminPage;