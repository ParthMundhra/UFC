import { useEffect, useState } from "react";
import FighterProfile from "./FighterProfile";

const divisions = [
  "Lightweight",
  "Welterweight",
  "Middleweight",
  "Bantamweight",
  "Featherweight",
  "Flyweight",
  "Light Heavyweight",
  "Heavyweight",
];

function DivisionRankings() {
  const [division, setDivision] = useState("Lightweight");
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFighter, setSelectedFighter] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/rankings/division/${division}`)
      .then((res) => res.json())
      .then((data) => {
        setRankings(data);
        setLoading(false);
      });
  }, [division]);

  // 👇 THIS MUST BE INSIDE THE FUNCTION
  if (selectedFighter) {
    return (
      <FighterProfile
        fighter={selectedFighter}
        onBack={() => setSelectedFighter(null)}
      />
    );
  }

  return (
  <div className="container">
    <h1>
      <span className="accent">{division}</span> Rankings
    </h1>

    <select
      value={division}
      onChange={(e) => setDivision(e.target.value)}
      style={{ marginBottom: "24px" }}
    >
      {divisions.map((d) => (
        <option key={d} value={d}>
          {d}
        </option>
      ))}
    </select>

    {loading && <p>Loading...</p>}

    {!loading && rankings.length === 0 && (
      <p className="meta">No ranked fighters yet.</p>
    )}

    {rankings.map((r, i) => (
      <div className="card" key={i}>
        <div style={{ display: "flex", alignItems: "center" }}>
          <div className="rank">#{i + 1}</div>
          <div
            className="fighter"
            onClick={() => setSelectedFighter(r.fighter)}
          >
            {r.fighter}
          </div>
        </div>

        <div className="meta">
          {r.avg_score} pts · {r.fights} fights
        </div>
      </div>
    ))}
  </div>
);
}
export default DivisionRankings;
