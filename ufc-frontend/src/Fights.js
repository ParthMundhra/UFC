import { useEffect, useState } from "react";
import FighterProfile from "./FighterProfile";

import API_BASE from "./api";


function Fights() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState("");
  const [fights, setFights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFighter, setSelectedFighter] = useState(null);

  // ---------------- LOAD EVENTS ----------------
  useEffect(() => {
    fetch(`${API_BASE}/events`)
      .then((res) => res.json())
      .then(setEvents)
      .catch(() => setEvents([]));
  }, []);

  // ---------------- LOAD FIGHTS ----------------
  useEffect(() => {
    setLoading(true);

    let url = `${API_BASE}/fights`;
    if (selectedEvent) {
      url += `?event=${encodeURIComponent(selectedEvent)}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setFights(data);
        setLoading(false);
      })
      .catch(() => {
        setFights([]);
        setLoading(false);
      });
  }, [selectedEvent]);

  // ---------------- FIGHTER PROFILE VIEW ----------------
  if (selectedFighter) {
    return (
      <FighterProfile
        fighter={selectedFighter}
        onBack={() => setSelectedFighter(null)}
      />
    );
  }

  // ---------------- MAIN VIEW ----------------
  return (
    <div style={{ padding: "20px", maxWidth: "1000px", margin: "0 auto" }}>
      <h2 style={{ marginBottom: "12px" }}>Fight Explorer</h2>

      {/* FILTERS */}
      <div style={{ marginBottom: "16px" }}>
        <select
          value={selectedEvent}
          onChange={(e) => setSelectedEvent(e.target.value)}
          style={{
            padding: "8px",
            minWidth: "260px",
            backgroundColor: "#111",
            color: "#fff",
            border: "1px solid #333",
            borderRadius: "6px",
          }}
        >
          <option value="">All Events</option>
          {events.map((e) => (
            <option key={e.name} value={e.name}>
              {e.name}
            </option>
          ))}
        </select>
      </div>

      {selectedEvent && (
  <p style={{ color: "#888", marginBottom: "20px" }}>
    Showing fights from <strong>{selectedEvent}</strong>
  </p>
)}

<p style={{ color: "#888", marginBottom: "10px" }}>
  {fights.length} fights found
</p>

      {/* RESULTS */}
      {loading ? (
        <p style={{ color: "#888" }}>Loading fights…</p>
      ) : fights.length === 0 ? (
        <p style={{ color: "#888" }}>
  No fights have been added for this event yet.
</p>

      ) : (
        fights.map((f, i) => (
          <div key={i} className="fight-card">
            <div className="fight-title">
              <span onClick={() => setSelectedFighter(f.red)}>
                {f.red}
              </span>
              {" vs "}
              <span onClick={() => setSelectedFighter(f.blue)}>
                {f.blue}
              </span>
            </div>

            <div className="fight-meta">
              {f.division} • {f.method} (R{f.round})
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Fights;
