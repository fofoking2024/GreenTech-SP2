# GreenTech E-Waste Recycling Platform (SP2)

## 🌍 Project Overview
GreenTech is a comprehensive, bilingual (English & Arabic) web application designed to manage **electronic waste (e-waste)** recycling. The platform bridges the gap between individuals who want to dispose of their old electronics responsibly and certified recycling companies with the infrastructure to process them.

By facilitating the secure and efficient handover of e-waste, GreenTech supports sustainability initiatives and promotes eco-friendly practices.

---

## ✨ Key Features

### 🏢 For Certified Recycling Companies
- **Dashboard & Analytics:** View real-time statistics, request statuses, and device types using interactive charts.
- **Collection Point Management:** Create, edit, and toggle physical drop-off locations (with Google Maps integration).
- **Order Management:** Process incoming recycling requests and update their statuses (`Received` ➔ `Under Recycling` ➔ `Recycled`).
- **Performance Reports:** Generate professional PDF reports (Monthly, Quarterly, Annually) using ReportLab.
- **Danger Zone:** Safely reset test data (requests and history) during development/testing phases.

### 👤 For Individual Users
- **AI-Powered Device Classifier:** An integrated, offline rule-based AI assistant that instantly categorizes devices from free-text descriptions and provides recyclability rates and tips.
- **Device Registration:** A streamlined, multi-step process to submit e-waste to specific company collection points.
- **Order Tracking:** Monitor the status of submitted recycling requests through a detailed timeline.
- **Rate Limiting:** Enforces a maximum of 10 requests per calendar month to prevent spam.

### 🌐 System-Wide Features
- **Bilingual Interface:** Full support for both English (LTR) and Arabic (RTL), easily toggled from the navigation bar.
- **Secure Authentication:** Role-based access control (User vs. Company) with hashed passwords via Werkzeug.

---

## 🛠️ Tech Stack
- **Backend Framework:** Python / [Flask](https://flask.palletsprojects.com/)
- **Database:** MySQL / SQLite (via [SQLAlchemy](https://www.sqlalchemy.org/) ORM)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Jinja2 Templates
- **PDF Generation:** [ReportLab](https://www.reportlab.com/)
- **Data Visualization:** Chart.js
- **Environment Management:** python-dotenv

---

## 📂 Project Architecture

The application follows a modular, Blueprint-based architecture for maintainability:

```text
SP2/
├── app.py                  # Application factory and entry point
├── config.py               # Environment configuration
├── extensions.py           # Shared SQLAlchemy database instance
├── models.py               # Database schemas and relationships
├── setup_db.py             # Script to initialize the MySQL database and tables
├── migrate_db.py           # Script to add missing columns to existing tables
├── .env                    # Environment variables (Database URL, Secret Key)
├── requirements.txt        # Python dependencies
│
├── routes/                 # Flask Blueprints
│   ├── auth.py             # Authentication (Login/Register for users & companies)
│   ├── user.py             # User portal and request submission
│   ├── company.py          # Company dashboard, points, and request management
│   ├── reports.py          # PDF report generation logic
│   └── ai.py               # AI classification API endpoints
│
├── utils/                  # Core Utilities
│   ├── translations.py     # Centralized English/Arabic translation dictionary
│   ├── ai_classifier.py    # Rule-based categorization and recommendation engine
│   └── helpers.py          # Assorted helpers (URL validation, etc.)
│
├── templates/              # Jinja2 HTML Templates
│   ├── index.html          # Landing page
│   ├── user-portal/        # User-facing views
│   └── company-portal/     # Company-facing views
│
└── static/                 # Static Assets
    ├── css/                # Stylesheets (including RTL support)
    └── images/             # Images and Icons
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server running locally (or adjust the `DATABASE_URL` in `.env` for SQLite)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SP2
   ```

2. **Create and activate a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Ensure your `.env` file contains the correct database URI. By default, it expects a local MySQL instance:
   ```env
   DATABASE_URL=mysql+pymysql://root:@localhost/greentech_db
   SECRET_KEY=YourSuperSecretKeyHere
   ```

5. **Initialize the Database**
   Run the setup script to create the database and all required tables:
   ```bash
   python setup_db.py
   ```
   *(If you are updating an existing database, you can run `python migrate_db.py` to add any newly introduced columns).*

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Platform**
   Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 👥 Authors & Acknowledgments
Built by the **SP2 Team** - GreenTech E-Waste Recycling Platform.
