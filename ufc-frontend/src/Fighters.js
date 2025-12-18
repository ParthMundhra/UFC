import { useEffect, useState } from "react";

function Fighters() {
  const [fighters, setFighters] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/fighters")
      .then((res) => res.json())
      .then((data) => setFighters(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>UFC Fighters</h1>

      {fighters.map((fighter) => (
        <div
          key={fighter.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "6px",
          }}
        >
          <h3>
            {fighter.name} ({fighter.nickname})
          </h3>
          <p>
            Record: {fighter.wins} - {fighter.losses}
          </p>
          <p>Division: {fighter.division}</p>
        </div>
      ))}
    </div>
  );
}

export default Fighters;
