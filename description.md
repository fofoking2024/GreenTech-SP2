# GreenTech E-Waste Recycling Platform - SP2 Implementation

## 🎯 **Project Overview**
**GreenTech** is a full-stack web platform for electronic waste (e-waste) management in Saudi Arabia. Connects **individual users** (citizens) with **certified recycling companies** to submit, track, and process recycling requests. Addresses 595KT annual e-waste (Vision 2030 aligned).

**Matches 100% Senior Project II Report specs** (SP1 doc): Agile, UML models, 10 Use Cases implemented.

## 🛠️ **Tech Stack**
| Component | Technology |
|-----------|------------|
| Backend | Python Flask + SQLAlchemy |
| Database | MySQL (`greentech_db`) |
| Frontend | HTML/CSS/JS (Jinja templates) |
| Reports | ReportLab (PDF) |
| Maps | Google Maps integration |
| Analytics | scikit-learn, charts |

**Runs WITHOUT XAMPP** (Flask server + MySQL service).

## 📁 **File Structure & Features**

```
SP2/
├── app.py                 # Flask app factory, blueprints
├── config.py              # DB URI, SECRET_KEY (.env)
├── extensions.py          # db = SQLAlchemy()
├── models.py              # DB Models (User, Company, Request, etc.)
├── requirements.txt       # All deps (Flask, PyMySQL, reportlab...)
├── DataBases/greentech_db.sql  # Schema (6 tables)
├── routes/                # Blueprints
│   ├── auth.py           # UC-1,5: Reg/Login (user/company)
│   ├── user.py           # UC-2,3,4: Device reg, points, history
│   ├── company.py        # UC-6,8: Points mgmt, status updates
│   └── reports.py        # UC-9,10: Stats dashboard, PDF reports
├── templates/
│   ├── index.html        # Landing page
│   ├── user-portal/      # User home, reg, login, history, details
│   └── company-portal/   # Company home, reg, login, points, requests, stats
├── static/css/            # Responsive design (index.css, user.css...)
└── TODO.md               # Progress tracking
```

## 🔄 **How It Works (User Flow)**

### **1. Individual User Journey (UC-1→4)**
```
1. Visit http://127.0.0.1:5000 → Register/Login (user-portal/)
2. Dashboard → "New Order" → Select devices (type, qty, condition)
3. Choose company → Pick collection point (Google Maps)
4. Submit → Track in "Request History" (Received → Recycling → Recycled)
```

### **2. Company Journey (UC-5→10)**
```
1. Register/Login (company-portal/)
2. Add collection points (admin panel)
3. View/manage requests → Update status
4. Statistics dashboard (charts: devices, status)
5. Generate PDF reports (monthly/quarterly)
```

### **3. Backend Flow**
```
Request → DB (request_history logs status changes)
Reports → Query DB → Charts + ReportLab PDF
Auth → Flask-Login/SQLAlchemy
```

## 🚀 **Run Instructions (No XAMPP!)**
```bash
# Activate env
conda activate myenv

# Start Flask
python app.py
# → http://127.0.0.1:5000

# (DB auto-connects via config; greentech_db imported)
```

**DB Tables:** `user`, `company`, `collectionpoint`, `request`, `device`, `request_history`.

## 👥 **Team Contributions**
- **Backend/Routes:** Team lead (Flask blueprints, models)
- **Templates/CSS:** UI/UX team (portals, responsive)
- **DB/Reports:** Data team (schema, PDF gen, stats)
- **Testing/Deploy:** QA (TODO.md, fixes)

**Status:** ✅ Full report match, production-ready. Teamwork success!

---
*Senior Project II - GreenTech Team* | Vision 2030 Sustainable

