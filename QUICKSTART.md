# Quick Start Guide - A-Player Hiring Suite

## Get Running in 5 Minutes

### Prerequisites Check

Ensure you have:
- ✅ Python 3.11+ installed (`python3 --version`)
- ✅ Node.js 18+ installed (`node --version`)
- ✅ Git installed
- ✅ A modern web browser

### Step 1: Install Backend Dependencies (2 minutes)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Build Frontend (2 minutes)

```bash
cd ../frontend
npm install
npm run build
```

### Step 3: Deploy Frontend to Backend (30 seconds)

```bash
# Mac/Linux
cp -r dist ../backend/static

# Windows
xcopy /E /I dist ..\backend\static
```

### Step 4: Launch Application (30 seconds)

**Mac/Linux:**
```bash
cd ..
./start.sh
```

**Windows:**
```cmd
cd ..
start.bat
```

The application will automatically open in your browser at `http://localhost:8000`

---

## What You'll See

1. **Dashboard** - Overview of your data
2. **Candidates** - Add your first candidate
3. **Scorecards** - Create your first A-Method scorecard
4. **Interviews** - Schedule biographical interviews
5. **CEO Assessments** - Assess leadership behaviors
6. **Power Score** - Evaluate leadership effectiveness
7. **Settings** - Backup and export options

---

## First Steps

1. **Add a Test Candidate**
   - Go to Candidates → Add Candidate
   - Fill in name and email
   - Click Save

2. **Create a Sample Scorecard**
   - Go to Scorecards → Create Scorecard
   - Add a role title (e.g., "Software Engineer")
   - Define mission, outcomes, and competencies
   - Export to PDF

3. **Try an Assessment**
   - Go to CEO Assessments → New Assessment
   - Rate across the four behaviors
   - View the results

---

## Troubleshooting

**Port 8000 in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
```

**Database errors?**
- Delete `backend/data/hiring_suite.db` and restart

**Frontend not showing?**
- Check that `backend/static/index.html` exists
- Rebuild frontend if needed

**Need API docs?**
- Visit `http://localhost:8000/api/docs`

---

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review [USER_GUIDE.md](USER_GUIDE.md) for methodology details
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design

---

## Quick Reference

**Stop the server**: Press `Ctrl+C` in the terminal

**Backup data**: Settings → Export SQLite Database

**Development mode**:
- Terminal 1: `cd backend && uvicorn app.main:app --reload`
- Terminal 2: `cd frontend && npm run dev`

---

**You're ready to start making evidence-based hiring and leadership decisions!**
