import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <div
      style={{
        backgroundColor: "#0a0a0a",
        borderBottom: "1px solid #222",
      }}
    >
      <div
        style={{
          maxWidth: "1000px",
          margin: "0 auto",
          padding: "14px 20px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {/* Logo */}
        <div style={{ fontWeight: "bold", fontSize: "18px" }}>
          <span style={{ letterSpacing: "0.5px" }}>
  UFC <span className="accent">Analytics</span>
</span>

        </div>

        {/* Links */}
        <div style={{ display: "flex", gap: "24px" }}>
          <NavLink
            to="/"
            style={({ isActive }) => ({
              color: isActive ? "#e10600" : "#eaeaea",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: isActive ? "600" : "400",
            })}
          >
            Home
          </NavLink>

          <NavLink
            to="/rankings"
            style={({ isActive }) => ({
              color: isActive ? "#e10600" : "#eaeaea",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: isActive ? "600" : "400",
            })}
          >
            Rankings
          </NavLink>

          <NavLink
            to="/fights"
            style={({ isActive }) => ({
              color: isActive ? "#e10600" : "#eaeaea",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: isActive ? "600" : "400",
            })}
          >
            Fights
          </NavLink>
        </div>
      </div>
    </div>
  );
}

export default Navbar;
