import { NavLink } from "react-router-dom";

export default function Navbar() {
  const activeStyle = {
    fontWeight: "bold",
    color: "#2e7d32",
  };

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "15px 40px",
        background: "#f8f9fa",
        borderBottom: "1px solid #ddd",
      }}
    >
      <h2>🌿 Plant Disease Detection</h2>

      <div
        style={{
          display: "flex",
          gap: "25px",
        }}
      >
        <NavLink
          to="/"
          style={({ isActive }) => (isActive ? activeStyle : {})}
        >
          Home
        </NavLink>

        <NavLink
          to="/history"
          style={({ isActive }) => (isActive ? activeStyle : {})}
        >
          History
        </NavLink>

        <NavLink
          to="/diseases"
          style={({ isActive }) => (isActive ? activeStyle : {})}
        >
          Diseases
        </NavLink>
      </div>
    </nav>
  );
}