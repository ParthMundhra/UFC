import { useEffect, useState } from "react";

function Fights() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState("");
  const [fights, setFights] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load all UFC events
  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then((res) => res.json())
      .then((data) => {
        setEvents(data);
        if (data.length > 0) setSelectedEvent(data[0]);
      });
  }, []);

  // Load fights for selected event
  useEffect(() => {
    if (!selectedEvent) return;

    setLoading(true);
    fetch(`http://127.0.0.1:8000/fights/event/${selectedEvent}`)
      .then((res) => res.json())
      .then((data) => {
        setFights(data);
        setLoading(false);
      });
  }, [selectedEvent]);

  return (
    <div className="container">
      <h1>Fight Explorer</h1>

      <select
        value={selectedEvent}
        onChange={(e) => setSelectedEvent(e.target.value)}
        style={{ marginBottom: "24px" }}
      >
        {events.map((e) => (
          <option key={e} value={e}>
            {e}
          </option>
        ))}
      </select>

      {loading && <p className="meta">Loading fights...</p>}

      {!loading && fights.length === 0 && (
        <p className="meta">No fights found for this event.</p>
      )}

      {fights.map((f, i) => (
        <div className="card" key={i}>
          <div>
            <strong>{f.red}</strong> vs <strong>{f.blue}</strong>
            <div className="meta">
              {f.division} · Round {f.round}
            </div>
          </div>

          <div className="meta">
            Winner: {f.winner} ({f.method})
          </div>
        </div>
      ))}
    </div>
  );
}

export default Fights;
