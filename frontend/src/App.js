import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import AddPatient from "./pages/AddPatient";
import MyPatients from "./pages/MyPatients";
import AddCard from "./pages/AddCard";

// Компонент для защиты приватных маршрутов
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("access_token");
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} /> {/* маршрут регистрации */}
        <Route path="/add-patient" element={<AddPatient />} />
        <Route path="/my-patients" element={<MyPatients />} />
        <Route path="/add-card" element={<AddCard />} />
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />
        {/* По умолчанию редирект на /login */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;