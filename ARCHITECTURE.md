# A-Player Hiring Suite - System Architecture

## Overview
The A-Player Hiring Suite is a local-first, browser-based desktop application that provides evidence-based hiring and leadership assessment tools. The application runs entirely on the user's local machine without requiring internet connectivity.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User's Browser                        │
│                     (http://localhost:8000)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         React + TypeScript Frontend (SPA)             │  │
│  │  ┌────────────┬────────────┬────────────┬──────────┐ │  │
│  │  │ Scorecard  │ Interview  │    CEO     │  Power   │ │  │
│  │  │ Generator  │  Scripting │ Behaviors  │  Score   │ │  │
│  │  └────────────┴────────────┴────────────┴──────────┘ │  │
│  │         Tailwind CSS + Headless UI Components         │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (JSON)
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend Server                     │
│                     (Python 3.11+)                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   API Endpoints                        │  │
│  │  /api/scorecards  /api/interviews  /api/assessments   │  │
│  │  /api/powerscore  /api/export      /api/backup        │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Business Logic Layer                    │  │
│  │  • Scorecard Service    • Interview Service           │  │
│  │  • Assessment Service   • Export Service (PDF)        │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Database Access Layer (ORM)              │  │
│  │                   SQLAlchemy                           │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    SQLite Database                           │
│                 (data/hiring_suite.db)                       │
│  ┌────────────┬────────────┬────────────┬──────────────┐   │
│  │ scorecards │ interviews │ candidates │ assessments  │   │
│  ├────────────┼────────────┼────────────┼──────────────┤   │
│  │ outcomes   │ questions  │   ratings  │   sessions   │   │
│  └────────────┴────────────┴────────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Desktop Packaging (Tauri)                       │
│  • Single executable for Windows/Mac/Linux                  │
│  • Auto-launches browser on startup                         │
│  • System tray integration                                  │
│  • Native file dialogs for backup/restore                   │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS v3
- **UI Components**: Headless UI (accessible components)
- **State Management**: React Context + Hooks
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **PDF Generation**: jsPDF + html2canvas
- **Forms**: React Hook Form + Zod validation
- **Icons**: Heroicons

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: SQLite 3
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **PDF Generation**: ReportLab
- **CORS**: FastAPI CORS middleware

### Desktop Packaging
- **Framework**: Tauri 1.5+
- **System**: Rust-based native wrapper
- **Benefits**:
  - Small bundle size (~3-5MB vs Electron's ~100MB)
  - Better security (no Node.js in production)
  - Native performance
  - Cross-platform (Windows, macOS, Linux)

## Core Modules

### 1. A-Method Scorecard Generator
**Purpose**: Create role-specific scorecards based on "Who: The A Method for Hiring"

**Features**:
- Define role mission (elevator pitch)
- Set 3-8 measurable outcomes
- Define 5-8 core competencies with behavioral indicators
- Save templates for common roles
- Export to PDF for sharing with hiring team
- Version history for scorecard iterations

**Data Model**:
```typescript
interface Scorecard {
  id: string;
  role_title: string;
  mission: string;
  outcomes: Outcome[];
  competencies: Competency[];
  created_at: Date;
  updated_at: Date;
}

interface Outcome {
  description: string;
  metric: string;
  timeframe: string;
}

interface Competency {
  name: string;
  definition: string;
  behavioral_indicators: string[];
}
```

### 2. Biographical Interview Scripting Tool
**Purpose**: Generate structured chronological interviews based on Topgrading methodology

**Features**:
- Upload/paste candidate work history
- Generate chronological interview script
- Include TORC (Threat of Reference Check) prompts
- Red flag detection guidance
- Note-taking interface during interview
- Session recording (notes only, no audio)
- Pattern analysis across jobs (reasons for leaving, accomplishments)

**Data Model**:
```typescript
interface Interview {
  id: string;
  candidate_id: string;
  created_at: Date;
  work_history: JobHistory[];
  notes: InterviewNote[];
  red_flags: RedFlag[];
}

interface JobHistory {
  company: string;
  title: string;
  start_date: Date;
  end_date: Date | null;
  responsibilities: string;
}

interface InterviewNote {
  job_id: string;
  question: string;
  response: string;
  timestamp: Date;
}
```

### 3. CEO Behaviors Leadership Assessor
**Purpose**: Evaluate leadership based on "The CEO Next Door" four key behaviors

**Features**:
- Assess four behaviors:
  1. **Decide with Speed and Conviction** (even with incomplete information)
  2. **Engage for Impact** (stakeholder management)
  3. **Relentless Reliability** (deliver consistently)
  4. **Adapt Boldly** (navigate change)
- Self-assessment and 360-degree observer ratings
- Visual radar chart of strengths/gaps
- Comparison to benchmark profiles
- Development recommendations per behavior

**Data Model**:
```typescript
interface CEOAssessment {
  id: string;
  subject_id: string;
  assessment_date: Date;
  assessment_type: 'self' | 'observer';
  ratings: BehaviorRating[];
  overall_score: number;
}

interface BehaviorRating {
  behavior: 'decisiveness' | 'reliability' | 'adaptation' | 'engagement';
  score: number; // 1-5 scale
  evidence: string[];
  development_notes: string;
}
```

### 4. Power Score Diagnostic Module
**Purpose**: Evaluate and track leadership effectiveness using "Power Score" framework

**Features**:
- Three core dimensions:
  1. **Results** (business outcomes delivered)
  2. **Relationships** (team and stakeholder trust)
  3. **Role Model** (values and integrity)
- Weighted scoring algorithm
- Gap analysis with actionable insights
- Longitudinal tracking over time
- Peer comparison (anonymized)
- Custom development plans

**Data Model**:
```typescript
interface PowerScoreAssessment {
  id: string;
  subject_id: string;
  assessment_date: Date;
  results_score: number;
  relationships_score: number;
  role_model_score: number;
  overall_power_score: number;
  dimension_details: DimensionDetail[];
  development_plan: DevelopmentItem[];
}

interface DimensionDetail {
  dimension: 'results' | 'relationships' | 'role_model';
  questions: QuestionResponse[];
  calculated_score: number;
}
```

## Database Schema (SQLite)

```sql
-- Core Entities
CREATE TABLE candidates (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    current_title TEXT,
    linkedin_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scorecards
CREATE TABLE scorecards (
    id TEXT PRIMARY KEY,
    role_title TEXT NOT NULL,
    mission TEXT NOT NULL,
    department TEXT,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scorecard_outcomes (
    id TEXT PRIMARY KEY,
    scorecard_id TEXT NOT NULL,
    description TEXT NOT NULL,
    metric TEXT,
    timeframe TEXT,
    priority INTEGER,
    FOREIGN KEY (scorecard_id) REFERENCES scorecards(id) ON DELETE CASCADE
);

CREATE TABLE scorecard_competencies (
    id TEXT PRIMARY KEY,
    scorecard_id TEXT NOT NULL,
    name TEXT NOT NULL,
    definition TEXT,
    FOREIGN KEY (scorecard_id) REFERENCES scorecards(id) ON DELETE CASCADE
);

CREATE TABLE competency_indicators (
    id TEXT PRIMARY KEY,
    competency_id TEXT NOT NULL,
    indicator TEXT NOT NULL,
    FOREIGN KEY (competency_id) REFERENCES scorecard_competencies(id) ON DELETE CASCADE
);

-- Interviews
CREATE TABLE interviews (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    scorecard_id TEXT,
    interview_date TIMESTAMP,
    interviewer_name TEXT,
    status TEXT DEFAULT 'scheduled',
    overall_rating TEXT,
    hire_recommendation BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (scorecard_id) REFERENCES scorecards(id)
);

CREATE TABLE job_history (
    id TEXT PRIMARY KEY,
    interview_id TEXT NOT NULL,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    sequence_order INTEGER,
    responsibilities TEXT,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
);

CREATE TABLE interview_questions (
    id TEXT PRIMARY KEY,
    job_history_id TEXT NOT NULL,
    question_type TEXT NOT NULL,
    question_text TEXT NOT NULL,
    response TEXT,
    rating INTEGER,
    notes TEXT,
    FOREIGN KEY (job_history_id) REFERENCES job_history(id) ON DELETE CASCADE
);

CREATE TABLE red_flags (
    id TEXT PRIMARY KEY,
    interview_id TEXT NOT NULL,
    flag_type TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT,
    job_history_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
);

-- CEO Behaviors Assessments
CREATE TABLE ceo_assessments (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    assessment_date TIMESTAMP NOT NULL,
    assessment_type TEXT NOT NULL,
    assessor_name TEXT,
    overall_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE ceo_behavior_ratings (
    id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    behavior TEXT NOT NULL,
    score INTEGER NOT NULL,
    evidence TEXT,
    development_notes TEXT,
    FOREIGN KEY (assessment_id) REFERENCES ceo_assessments(id) ON DELETE CASCADE
);

-- Power Score Assessments
CREATE TABLE power_score_assessments (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    assessment_date TIMESTAMP NOT NULL,
    results_score REAL NOT NULL,
    relationships_score REAL NOT NULL,
    role_model_score REAL NOT NULL,
    overall_power_score REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE power_score_responses (
    id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    dimension TEXT NOT NULL,
    question_id TEXT NOT NULL,
    question_text TEXT NOT NULL,
    response_value INTEGER,
    response_text TEXT,
    FOREIGN KEY (assessment_id) REFERENCES power_score_assessments(id) ON DELETE CASCADE
);

CREATE TABLE development_plans (
    id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    dimension TEXT NOT NULL,
    goal TEXT NOT NULL,
    action_steps TEXT,
    target_date DATE,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (assessment_id) REFERENCES power_score_assessments(id) ON DELETE CASCADE
);

-- System tables
CREATE TABLE app_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE export_history (
    id TEXT PRIMARY KEY,
    export_type TEXT NOT NULL,
    file_path TEXT,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Candidates
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create new candidate
- `GET /api/candidates/{id}` - Get candidate details
- `PUT /api/candidates/{id}` - Update candidate
- `DELETE /api/candidates/{id}` - Delete candidate

### Scorecards
- `GET /api/scorecards` - List all scorecards
- `POST /api/scorecards` - Create new scorecard
- `GET /api/scorecards/{id}` - Get scorecard details
- `PUT /api/scorecards/{id}` - Update scorecard
- `DELETE /api/scorecards/{id}` - Delete scorecard
- `GET /api/scorecards/{id}/export/pdf` - Export scorecard to PDF

### Interviews
- `GET /api/interviews` - List all interviews
- `POST /api/interviews` - Create new interview
- `GET /api/interviews/{id}` - Get interview details
- `PUT /api/interviews/{id}` - Update interview
- `DELETE /api/interviews/{id}` - Delete interview
- `POST /api/interviews/{id}/generate-script` - Generate interview script
- `GET /api/interviews/{id}/export/pdf` - Export interview notes to PDF

### CEO Assessments
- `GET /api/ceo-assessments` - List all assessments
- `POST /api/ceo-assessments` - Create new assessment
- `GET /api/ceo-assessments/{id}` - Get assessment details
- `PUT /api/ceo-assessments/{id}` - Update assessment
- `DELETE /api/ceo-assessments/{id}` - Delete assessment
- `GET /api/ceo-assessments/{id}/export/pdf` - Export assessment report

### Power Score
- `GET /api/power-score` - List all assessments
- `POST /api/power-score` - Create new assessment
- `GET /api/power-score/{id}` - Get assessment details
- `PUT /api/power-score/{id}` - Update assessment
- `GET /api/power-score/{id}/trends` - Get historical trends
- `GET /api/power-score/{id}/export/pdf` - Export assessment report

### System
- `POST /api/backup/export` - Export entire database
- `POST /api/backup/import` - Import database backup
- `GET /api/health` - Health check endpoint

## Local Deployment Workflow

### Development Mode
1. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev  # Runs on localhost:5173, proxies to :8000
   ```

### Production Build
1. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   # Outputs to frontend/dist
   ```

2. **Copy Frontend to Backend**:
   ```bash
   cp -r frontend/dist backend/static
   ```

3. **Run Production Server**:
   ```bash
   cd backend
   python run.py
   # Opens browser automatically to http://localhost:8000
   ```

### Desktop Packaging (Tauri)
1. **Install Tauri CLI**:
   ```bash
   npm install -g @tauri-apps/cli
   ```

2. **Build Desktop App**:
   ```bash
   cd desktop
   tauri build
   # Outputs platform-specific executables to desktop/target/release
   ```

3. **Distribution**:
   - Windows: `.exe` installer + portable `.exe`
   - macOS: `.app` bundle + `.dmg` installer
   - Linux: `.AppImage`, `.deb`, `.rpm`

## Security & Privacy

### Data Security
- All data stored locally in SQLite database
- Database file encrypted at rest (optional, OS-level)
- No external network calls
- No telemetry or analytics

### Access Control
- Single-user application (no authentication needed)
- Optional password protection for database file
- Export files can be encrypted with user-provided password

### Audit Trail
- All create/update/delete operations logged with timestamps
- Export history tracked
- No PII sent externally

## Performance Considerations

### Frontend Optimization
- Code splitting by route
- Lazy loading of heavy components
- Virtual scrolling for large lists
- Debounced search inputs
- Memoized expensive calculations

### Backend Optimization
- Database indexes on frequently queried fields
- Connection pooling
- Caching of static data
- Pagination for large result sets
- Background processing for PDF generation

### Storage
- Expected database size: ~10-50MB for 100 candidates
- Automatic database vacuum on backup
- Optional data archival for old assessments

## Extensibility

### Plugin Architecture (Future)
- Custom assessment templates
- Third-party integrations (with user permission)
- Custom report templates
- Import from external HR systems

### White-Label Potential
- Configurable branding
- Custom color schemes
- Organization-specific templates
- Logo customization

## Testing Strategy

### Backend
- Unit tests: pytest
- API tests: TestClient
- Database tests: in-memory SQLite
- Coverage target: >80%

### Frontend
- Unit tests: Vitest
- Component tests: React Testing Library
- E2E tests: Playwright
- Coverage target: >70%

### Integration
- End-to-end workflow tests
- Cross-browser compatibility
- Performance benchmarking

## Documentation

### User Documentation
- Quick start guide
- Feature tutorials with screenshots
- Video walkthroughs
- Methodology background (summaries of source books)
- FAQ

### Developer Documentation
- API reference
- Database schema docs
- Component storybook
- Contributing guide
- Build and deployment guide

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Maintained By**: A-Player Hiring Suite Team
