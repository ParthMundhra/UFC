# UFC Analytics Platform 🥊

UFC Analytics is a full-stack web application that centralizes UFC fight data into a single platform.  
It brings together events, fights, fighters, and division-based rankings that are otherwise scattered across multiple sources.

The system is designed to scale toward the complete UFC event history while maintaining structured, queryable, and consistent data.

---

## 🌐 Live Demo

https://ufcanalytics.netlify.app

---

## 🚀 Features

- 📥 Automated ingestion of UFC events from Wikipedia
- 🧹 Fighter name normalization (no duplicates like `(c)`)
- 🗂️ PostgreSQL relational database (fighters & fights)
- 🥋 Division-based rankings (Lightweight, Welterweight, etc.)
- ⚖️ Fair scoring model (win + finish bonus + 5-round bonus)
- 📊 Normalized rankings (average score per fight)
- 🧑‍🤝‍🧑 Fighter profile pages with fight history
- 🌐 Interactive React frontend with division dropdown

---

## 🛠 Tech Stack

**Backend**
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

**Frontend**
- React
- JavaScript
- Fetch API

**Data**
- Wikipedia scraping
- Pandas
- BeautifulSoup
