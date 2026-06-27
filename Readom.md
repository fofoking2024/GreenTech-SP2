
```markdown
# GreenTech E-Waste Recycling Platform (SP2)

GreenTech is a comprehensive, bilingual (English & Arabic) web application designed to manage **electronic waste (e-waste)** recycling. The platform bridges the gap between individuals who want to dispose of their old electronics responsibly and certified recycling companies with the infrastructure to process them. By facilitating the secure and efficient handover of e-waste, GreenTech supports sustainability initiatives and promotes eco-friendly practices.

## 🎯 Project Overview

GreenTech is a full-stack web platform for electronic waste (e-waste) management in Yemen. It connects **individual users** (citizens) with **certified recycling companies** to submit, track, and process recycling requests. This project addresses the local e-waste challenges, aligning with environmental sustainability goals and promoting a digital circular economy. The implementation matches 100% of the Senior Project II Report specifications, incorporating Agile methodologies, UML models, and 10 implemented Use Cases.

## 🖼️ System Interface & Visual Walkthrough

### 1. System Landing Page (Main Interface)
The main landing page serves as the primary gateway, presenting the platform's core mission, dual-portal entry points (User vs. Company), and bilingual switching capabilities to maximize public engagement.
![Main Landing Page](static/images/Screenshot%202026-06-27%20231428.png)

### 2. Secure Authentication Portal
A unified, role-based secure login interface enforcing cryptographic credential validation via Werkzeug to guarantee robust access control parameters.
![Login Page](static/images/Screenshot%202026-06-27%20231516.png)

### 3. Streamlined Device Registration Pipeline
A multi-tiered wizard form that allows individual users to intuitively catalog their electronic assets, input condition metrics, and initiate a recycling transaction.
![Device Registration Page](static/images/Screenshot%202026-06-27%20231555.png)

### 4. Comprehensive Request Details & Asset Diagnostics
A granular look into the submitted transaction, detailing asset specifications, historical lifecycle tracking, and device diagnostics under review.
#### Part I: Asset Specifications
![Request Details Part 1](static/images/Screenshot%202026-06-27%20231836.png)
#### Part II: Evaluation Metrics & Logistics
![Request Details Part 2](static/images/Screenshot%202026-06-27%20231802.png)

### 5. Automated System Notifications & Timeline Logs
An automated state-machine logger providing real-time notification alerts and transparency milestones regarding the status of pending user submissions.
![Order Notifications](static/images/Screenshot%202026-06-27%20232404.png)

### 6. Order Lifecycle State: Transition to 'Recycled'
Visual verification showing the terminal state of a specific request, mapping the transition tracking from initial submission to the final eco-friendly `Recycled` milestone.
![Recycled State](static/images/Screenshot%202026-06-27%20232418.png)

### 7. Corporate Administrative Control Panel
The master dashboard for certified companies, offering centralized management vectors for active drop-off logistics, request processing, interactive tools, and data reporting.
![Company Dashboard](static/images/Screenshot%202026-06-27%20232311.png)

### 8. Statistical Data Visualization & Analytics Engine
An analytical dashboard rendering distribution metrics via Chart.js, visualizing status ratios through pie charts and tracking electronic categories using progressive bar charts.
![Statistical Analytics](static/images/Screenshot%202026-06-27%20232528.png)

### 9. PDF Report Generation & Compliance Export
An integrated document compilation system leveraging ReportLab to build and export institutional-grade, formal data reports for external compliance bodies.
![Report Generation](static/images/Screenshot%202026-06-27%20232631.png)

## ✨ Key Features

### 🏢 For Certified Recycling Companies
* **Dashboard & Analytics:** View real-time statistics, request statuses, and device types using interactive charts.
* **Collection Point Management:** Create, edit, and toggle physical drop-off locations with Google Maps integration.
* **Order Management:** Process incoming recycling requests and update their statuses (`Received` ➔ `Under Recycling` ➔ `Recycled`).
* **Performance Reports:** Generate professional PDF reports (Monthly, Quarterly, Annually) using ReportLab.
* **Danger Zone:** Safely reset test data (requests and history) during development/testing phases.

### 👤 For Individual Users
* **AI-Powered Device Classifier:** An integrated, offline rule-based AI assistant that instantly categorizes devices from free-text descriptions and provides recyclability rates and tips.
* **Device Registration:** A streamlined, multi-step process to submit e-waste to specific company collection points.
* **Order Tracking:** Monitor the status of submitted recycling requests through a detailed timeline.
* **Rate Limiting:** Enforces a maximum of 10 requests per calendar month to prevent spam.

### 🌐 System-Wide Features
* **Bilingual Interface:** Full support for both English (LTR) and Arabic (RTL), easily toggled from the navigation bar.
* **Secure Authentication:** Role-based access control (User vs. Company) with hashed passwords via Werkzeug.

## 🛠️ Tech Stack

| Component | Technology |
| :-------- | :----------------------------------- |
| Backend   | Python Flask + SQLAlchemy            |
| Database  | MySQL (greentech_db)                  |
| Frontend  | HTML/CSS/JS (Jinja templates)        |
| Reports   | ReportLab (PDF)                      |
| Maps      | Google Maps integration              |
| Analytics | scikit-learn, Chart.js               |

The application runs seamlessly utilizing a native Flask web server architecture and a centralized MySQL service.

## 📁 File Structure


```

SP2/
├── app.py                      # Flask app factory, blueprints
├── config.py                   # DB URI, SECRET_KEY (.env)
├── extensions.py               # db = SQLAlchemy()
├── models.py                   # DB Models (User, Company, Request, etc.)
├── requirements.txt            # All dependencies (Flask, PyMySQL, reportlab...)
├── DataBases/greentech_db.sql  # Schema (6 tables)
├── routes/                     # Blueprints for different functionalities
│   ├── auth.py                # UC-1,5: Registration/Login (user/company)
│   ├── user.py                # UC-2,3,4: Device registration, collection points, history
│   ├── company.py             # UC-6,8: Collection points management, status updates
│   └── reports.py             # UC-9,10: Statistics dashboard, PDF reports
├── templates/                  # HTML templates
│   ├── index.html             # Landing page
│   ├── user-portal/           # User home, registration, login, history, details
│   └── company-portal/        # Company home, registration, login, collection points, requests, statistics
├── static/css/                 # Responsive design stylesheets (index.css, user.css...)
└── TODO.md                     # Progress tracking

```

## 🔄 How It Works (User Flow)

### 1. Individual User Journey (UC-1→4)
1. Visit `http://127.0.0.1:5000` ➔ Register/Login (user-portal/)
2. Dashboard ➔ "New Order" ➔ Select devices (type, quantity, condition)
3. Choose company ➔ Pick collection point (Google Maps)
4. Submit ➔ Track in "Request History" (Received ➔ Recycling ➔ Recycled)

### 2. Company Journey (UC-5→10)
1. Register/Login (company-portal/)
2. Add collection points (admin panel)
3. View/manage requests ➔ Update status
4. Statistics dashboard (charts: devices, status)

## 🚀 Installation and Setup

To set up the GreenTech E-Waste Recycling Platform locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/fofoking2024/GreenTech-SP2.git](https://github.com/fofoking2024/GreenTech-SP2.git)
   cd GreenTech-SP2

```

2. **Create a virtual environment and activate it:**
```bash
python3 -m venv venv
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Database Setup:**
* Ensure you have MySQL installed and running.
* Import the `greentech_db.sql` file located in the `DataBases/` directory into your MySQL server.
* Update the database connection string in `config.py` to match your MySQL configuration.


5. **Run the application:**
```bash
python app.py

```


The application will be accessible at `http://127.0.0.1:5000`.

## 🤝 Contributing

Contributions are welcome! Please feel free to fork the repository, create a new branch, and submit a pull request for any improvements or bug fixes.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact & Support

* **Phone:** +967777688809
* * **📧:** faresalselwi1@gmail.com 
* **Inquiries:** For any issues or technical support, please open an issue directly in the GitHub repository.

```
