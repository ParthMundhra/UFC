import { useEffect, useState } from "react";
import { cache } from "./cache";
import API_BASE from "./api";

function FighterProfile({ fighter, onBack }) {
  const [data, setData] = useState(null);
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch fighter profile
  useEffect(() => {
    setLoading(true);

    fetch(`${API_BASE}/${fighter}`)
      .then((res) => res.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => {
        setData(null);
        setLoading(false);
      });
  }, [fighter]);

  // Fetch & cache fighter image
  useEffect(() => {
    if (cache.fighterImages[fighter]) {
      setImage(cache.fighterImages[fighter]);
      return;
    }

    fetch(`${API_BASE}/fighter-image/${fighter}`)
      .then((res) => res.json())
      .then((d) => {
        cache.fighterImages[fighter] = d.image;
        setImage(d.image);
      })
      .catch(() => setImage(null));
  }, [fighter]);

  if (loading) {
    return (
      <div className="container">
        <p className="meta">Loading fighter profile…</p>
      </div>
    );
  }

  if (!data || data.error) {
    return (
      <div className="container">
        <button onClick={onBack}>← Back</button>
        <p className="meta">Fighter not found.</p>
      </div>
    );
  }

  return (
    <div className="container">
      <button onClick={onBack}>← Back</button>

      {/* HEADER */}
      <div style={{ marginTop: "20px" }}>
        {image && (
          <img
            src={image}
            alt={data.name}
            onError={(e) => (e.target.style.display = "none")}
            style={{
              width: "180px",
              borderRadius: "12px",
              marginBottom: "16px",
              backgroundColor: "#111",
            }}
          />
        )}

        <h1>{data.name}</h1>
        <p className="meta">
          Record: {data.wins}–{data.losses} · {data.total_fights} fights
        </p>
        <p className="meta">
  Finishes: {data.finish_wins} · Decisions: {data.decision_wins} ·
  Finish rate: {data.finish_rate}%
</p>

      </div>

      {/* HISTORY */}
      <h2 style={{ marginTop: "32px" }}>Fight History</h2>

      {data.history.length === 0 && (
        <p className="meta">No fights recorded.</p>
      )}

      {data.history.map((f, i) => (
        <div className="card" key={i}>
          <div>
            <strong>{f.result}</strong> vs {f.opponent}
            <div className="meta">
              {f.method} · {f.division}
            </div>
          </div>

          <div className="meta">{f.event}</div>
        </div>
      ))}
    </div>
  );
}

export default FighterProfile;
