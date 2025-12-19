import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { cache } from "./cache";



function Home() {
  const navigate = useNavigate();

  // NEWS STATE
  const [news, setNews] = useState(cache.news || []);
  const [loadingNews, setLoadingNews] = useState(!cache.news);



  // PLATFORM STATS STATE
  const [stats, setStats] = useState({
    fights: 0,
    events: 0,
    divisions: 0,
    loading: true,
  });

  // ---------------- FETCH NEWS (CACHED) ----------------
  useEffect(() => {
    if (cache.news) {
      setNews(cache.news);
      setLoadingNews(false);
      return;
    }

    fetch("http://127.0.0.1:8000/news")
      .then((res) => res.json())
      .then((data) => {
        cache.news = data;
        setNews(data);
        setLoadingNews(false);
      })
      .catch(() => {
        setNews([]);
        setLoadingNews(false);
      });
  }, []);

  // ---------------- FETCH PLATFORM STATS ----------------
  useEffect(() => {
    async function loadStats() {
      try {
        const fightsRes = await fetch("http://127.0.0.1:8000/fights");
        const fights = await fightsRes.json();

        const eventsRes = await fetch("http://127.0.0.1:8000/events");
        const events = await eventsRes.json();

        const divisions = new Set(
          fights.map((f) => f.division).filter(Boolean)
        );

        setStats({
          fights: fights.length,
          events: events.length,
          divisions: divisions.size,
          loading: false,
        });
      } catch {
        setStats({
          fights: 0,
          events: 0,
          divisions: 0,
          loading: false,
        });
      }
    }

    loadStats();
  }, []);

  return (
    <div className="container">
      {/* HERO */}
      <div className="hero">
        <h1 style={{ fontSize: "42px" }}>
          UFC <span className="accent">Analytics</span>
        </h1>

        <p className="meta" style={{ maxWidth: "650px", marginTop: "12px" }}>
          UFC Analytics is a centralized platform that aggregates official UFC fight data
across events and weight divisions, enabling structured exploration of fighters,
matchups, and outcomes through a clean analytical interface.

        </p>
      </div>

      {/* NAVIGATION CARDS */}
      <div className="section">
        <h2>Explore</h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: "16px",
            marginTop: "16px",
          }}
        >
          <div
            className="card"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/rankings")}
          >
            <strong>Division Rankings</strong>
            <p className="meta" style={{ marginTop: "6px" }}>
              Performance-based rankings by weight class.
            </p>
          </div>

          <div
            className="card"
            style={{ cursor: "pointer" }}
            onClick={() => navigate("/fights")}
          >
            <strong>Fight Explorer</strong>
            <p className="meta" style={{ marginTop: "6px" }}>
              Browse complete UFC fight cards by event.
            </p>
          </div>
        </div>
      </div>

      {/* NEWS */}
      <div className="section">
        <h2>Latest UFC News</h2>

        {loadingNews && <p className="meta">Loading latest news…</p>}

        {!loadingNews && news.length === 0 && (
          <p className="meta">News unavailable right now.</p>
        )}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "16px",
            marginTop: "16px",
          }}
        >
          {news.map((n, i) => (
            <a
              key={i}
              href={n.url}
              target="_blank"
              rel="noreferrer"
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <div className="card" style={{ padding: 0, overflow: "hidden" }}>
                {n.image && (
                  <img
                    src={n.image}
                    alt={n.title}
                    onError={(e) => (e.target.style.display = "none")}
                    style={{
                      width: "100%",
                      height: "160px",
                      objectFit: "cover",
                      backgroundColor: "#111",
                    }}
                  />
                )}

                <div style={{ padding: "16px" }}>
                  <strong>{n.title}</strong>
                  <div className="meta">{n.source}</div>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* PLATFORM SNAPSHOT */}
      <div className="section">
        <h2>Platform Snapshot</h2>

        <div className="stat-grid">
          <div className="stat-card">
            <div className="stat-number">
              {stats.loading ? "—" : stats.fights}
            </div>
            <div className="stat-label">UFC Fights Indexed</div>
          </div>

          <div className="stat-card">
            <div className="stat-number">
              {stats.loading ? "—" : stats.events}
            </div>
            <div className="stat-label">UFC Events Covered</div>
          </div>

          <div className="stat-card">
            <div className="stat-number">
              {stats.loading ? "—" : stats.divisions}
            </div>
            <div className="stat-label">Weight Divisions Tracked</div>
          </div>

          <div className="stat-card">
            <div className="stat-number">Unified</div>
            <div className="stat-label">Centralized Fight Dataset</div>
          </div>
        </div>
      </div>

      {/* ABOUT AUTHOR */}
      <div className="section">
        <h2>About the Author</h2>

        <div className="card">
          <p className="meta" style={{ marginBottom: "12px" }}>
            Built by <strong>Parth Mundhra</strong>
          </p>

          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
            <a
              href="https://github.com/ParthMundhra"
              target="_blank"
              rel="noreferrer"
              className="accent"
            >
              GitHub
            </a>

            <a
              href="https://www.linkedin.com/in/parthmundhra/"
              target="_blank"
              rel="noreferrer"
              className="accent"
            >
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
