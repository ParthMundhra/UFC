# UFC Analytics Platform 🥊

A full-stack UFC analytics platform that scrapes real fight data from Wikipedia,
stores it in PostgreSQL, and generates division-based fighter rankings using
custom scoring logic.

Built to explore **data ingestion, normalization, analytics, and full-stack development**.

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

## 🧠 Ranking Logic (Simplified)

- Win: +10 points  
- KO / TKO: +6  
- Submission: +5  
- Decision: +2  
- 5-round fight bonus: +2  
- Rankings normalized by number of fights  
- Minimum fight threshold enforced  

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

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repo
git clone https://github.com/ParthMundhra/UFC.git
cd UFC

### 2️⃣ Backend setup
- cd ufc-backend
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- uvicorn main:app --reload

### 3️⃣ Fronted setup
- cd ufc-frontend
- npm install
- npm start
