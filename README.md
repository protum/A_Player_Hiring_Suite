# A-Player Hiring Suite

## Evidence-Based Hiring and Leadership Assessment Platform

A-Player Hiring Suite is a **local-first, browser-based desktop application** that translates evidence-based hiring and leadership assessment methodologies into an intuitive interface that runs entirely on your laptop or desktop—without requiring internet connectivity or cloud services.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

---

## 🎯 Purpose

Replace subjective hiring and leadership evaluation practices with a **disciplined, repeatable, and locally executed system** that HR professionals, hiring managers, and leadership coaches can run securely on their own devices.

---

## 📚 Core Methodologies

This application implements frameworks from authoritative works:

- **Who: The A Method for Hiring** - Geoff Smart & Randy Street
- **Topgrading** - Bradford D. Smart
- **Foolproof Hiring** - Karen Kocher
- **The CEO Next Door** - Elena L. Botelho & Kim R. Powell
- **Power Score** - Leadership effectiveness assessment

---

## ✨ Key Features

### 1. A-Method Scorecard Generator
Create and manage role-specific scorecards with:
- Role mission statements
- 3-8 measurable outcomes
- 5-8 core competencies with behavioral indicators
- PDF export for sharing with hiring teams
- Template library for common roles

### 2. Biographical Interview Scripting Tool
Generate chronological interview scripts based on:
- Topgrading methodology
- Candidate work history
- TORC (Threat of Reference Check) prompts
- Red flag detection guidance
- Note-taking interface during interviews

### 3. CEO Behaviors Leadership Assessor
Evaluate leadership across four key behaviors:
- **Decisiveness** - Decide with speed and conviction
- **Reliability** - Deliver consistently
- **Adaptation** - Navigate change boldly
- **Engagement** - Build stakeholder relationships

Features:
- Self and 360-degree assessments
- Visual scoring summaries
- Development recommendations

### 4. Power Score Diagnostic Module
Assess leadership effectiveness across three dimensions:
- **Results** - Business outcomes delivered
- **Relationships** - Team and stakeholder trust
- **Role Model** - Values and integrity

Features:
- Gap analysis and scoring
- Longitudinal tracking
- Development planning
- Trend visualization

### 5. Data Management
- **Local Storage** - All data stored in SQLite database on your device
- **Backup/Export** - Export database or JSON for backup
- **Import/Restore** - Restore from previous backups
- **PDF Reports** - Export assessments and scorecards to PDF
- **No Telemetry** - Zero external data transmission

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** and npm (for development only)
- **Web browser** (Chrome, Firefox, Edge, or Safari)

### Installation

#### Option 1: Production Mode (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd A_Player_Hiring_Suite
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Build the frontend:**
   ```bash
   cd ../frontend
   npm install
   npm run build
   ```

4. **Copy frontend build to backend:**
   ```bash
   cp -r dist ../backend/static
   ```

5. **Run the application:**
   ```bash
   cd ../backend
   python run.py
   ```

6. **Access the application:**
   - The app will automatically open in your default browser at `http://localhost:8000`
   - If it doesn't open automatically, navigate to `http://localhost:8000` manually

#### Option 2: Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access at `http://localhost:5173` (automatically proxies to backend)

---

## 📖 User Guide

### Getting Started

1. **Launch the Application**
   - Run `python backend/run.py`
   - Your browser will open to the dashboard

2. **Add Your First Candidate**
   - Navigate to "Candidates" in the sidebar
   - Click "Add Candidate"
   - Fill in candidate details (name, email, etc.)
   - Click "Save Candidate"

3. **Create a Role Scorecard**
   - Navigate to "Scorecards"
   - Click "Create Scorecard"
   - Define the role mission
   - Add 3-8 measurable outcomes
   - Define 5-8 core competencies
   - Export to PDF for your hiring team

4. **Schedule an Interview**
   - Navigate to "Interviews"
   - Click "Schedule Interview"
   - Select candidate and scorecard
   - Add work history to generate chronological script
   - Use TORC prompts during interview
   - Flag concerns as they arise

5. **Conduct Assessments**
   - **CEO Behaviors**: Navigate to "CEO Assessments" → Rate across 4 behaviors
   - **Power Score**: Navigate to "Power Score" → Complete dimension questions

### Data Management

#### Backup Your Data

1. Navigate to "Settings"
2. Under "Data Backup & Export":
   - Click "Export SQLite Database" for full backup
   - Click "Export JSON" for portable format
3. Save the file to a secure location

#### Restore from Backup

1. Navigate to "Settings"
2. Under "Import Database":
   - Click "Import Backup"
   - Select your `.db` or `.json` file
   - Confirm the import
3. Refresh the page

⚠️ **Warning**: Importing will overwrite all existing data. Always backup first!

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- ReportLab (PDF generation)
- Uvicorn (ASGI server)

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- Vite for build tooling

**Data Storage:**
- SQLite database at `backend/data/hiring_suite.db`
- All data stored locally on your filesystem
- No external dependencies

### Project Structure

```
A_Player_Hiring_Suite/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── data/             # SQLite database
│   ├── static/           # Frontend build (production)
│   ├── requirements.txt
│   └── run.py            # Launch script
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── types/        # TypeScript types
│   │   └── App.tsx       # Main app
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   └── (documentation files)
├── ARCHITECTURE.md       # Detailed architecture
└── README.md            # This file
```

---

## 🔒 Security & Privacy

### Data Security
- ✅ All data stored locally (no cloud, no servers)
- ✅ SQLite database on your filesystem
- ✅ No external network calls
- ✅ No telemetry or analytics
- ✅ No PII sent anywhere

### Optional Enhancements
- Encrypt database file using OS-level encryption
- Use full-disk encryption on your device
- Password-protect exported backups

---

## 🛠️ Development

### Running Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Code Quality

**Backend:**
```bash
cd backend
black app/  # Code formatting
mypy app/   # Type checking
```

**Frontend:**
```bash
cd frontend
npm run lint  # ESLint
```

### Database Migrations

To modify the database schema:

1. Update models in `backend/app/models/`
2. Create migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Description"
   ```
3. Apply migration:
   ```bash
   alembic upgrade head
   ```

---

## 📊 API Documentation

When running the backend, access interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

### Key Endpoints

**Candidates:**
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create candidate
- `GET /api/candidates/{id}` - Get candidate details
- `PUT /api/candidates/{id}` - Update candidate
- `DELETE /api/candidates/{id}` - Delete candidate

**Scorecards:**
- `GET /api/scorecards` - List all scorecards
- `POST /api/scorecards` - Create scorecard
- `GET /api/scorecards/{id}/export/pdf` - Export to PDF

**Interviews:**
- `GET /api/interviews` - List all interviews
- `POST /api/interviews` - Create interview
- `POST /api/interviews/{id}/generate-script` - Generate interview script
- `POST /api/interviews/{id}/red-flags` - Add red flag

**Assessments:**
- `POST /api/assessments/ceo` - Create CEO assessment
- `POST /api/assessments/power-score` - Create Power Score assessment
- `GET /api/assessments/power-score/{id}/trends` - Get trends

**System:**
- `GET /api/system/health` - Health check
- `POST /api/system/backup/export` - Export backup
- `POST /api/system/backup/import` - Import backup
- `GET /api/system/stats` - Get statistics

---

## 🎨 Customization

### Branding

To customize branding:

1. **Colors** - Edit `frontend/tailwind.config.js`:
   ```javascript
   theme: {
     extend: {
       colors: {
         primary: { /* your colors */ }
       }
     }
   }
   ```

2. **Logo** - Replace logo in `frontend/src/assets/`

3. **App Name** - Update in:
   - `frontend/index.html` (title)
   - `frontend/src/App.tsx` (navigation)
   - `backend/app/main.py` (API title)

---

## 🚢 Deployment

### Desktop Packaging (Future Enhancement)

Package as a standalone desktop app using Tauri:

```bash
cd desktop
npm install -g @tauri-apps/cli
tauri build
```

This will create:
- **Windows**: `.exe` installer
- **macOS**: `.app` bundle + `.dmg`
- **Linux**: `.AppImage`, `.deb`, `.rpm`

---

## 📝 Troubleshooting

### Database Locked Error

If you see "database is locked":
1. Close all instances of the application
2. Restart the backend server
3. If persists, delete `backend/data/hiring_suite.db` and restart

### Port Already in Use

If port 8000 is in use:
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000    # Windows
```

### Frontend Not Loading

1. Check that backend is running on port 8000
2. Check browser console for errors
3. Clear browser cache and reload
4. Rebuild frontend: `cd frontend && npm run build`

---

## 🤝 Contributing

This is a local-first application designed for private use. If you wish to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with clear description

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙏 Acknowledgments

This application implements methodologies from:

- Geoff Smart & Randy Street - *Who: The A Method for Hiring*
- Bradford D. Smart - *Topgrading*
- Karen Kocher - *Foolproof Hiring*
- Elena L. Botelho & Kim R. Powell - *The CEO Next Door*
- Power Score methodology authors

---

## 📞 Support

For issues or questions:
1. Check this README and ARCHITECTURE.md
2. Review the API documentation at `/api/docs`
3. Check the troubleshooting section above

---

## 🗺️ Roadmap

Future enhancements:
- [ ] Tauri desktop packaging for one-click install
- [ ] Custom assessment templates
- [ ] Advanced reporting and analytics
- [ ] Interview scheduling integration
- [ ] Team collaboration features (optional)
- [ ] Mobile companion app for note-taking

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Status**: Production Ready

**Run locally. Store locally. Own your data.**
