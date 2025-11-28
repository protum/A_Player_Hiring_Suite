# A-Player Hiring Suite - System Architecture

## Overview
The A-Player Hiring Suite is a comprehensive SaaS platform integrating five premier executive hiring and leadership assessment frameworks into a unified system.

## Frameworks Integrated
1. **Who: The A Method for Hiring** - Scorecard-based hiring
2. **Topgrading** - Chronological in-depth structured interviews
3. **Foolproof Hiring** - Evidence-based candidate evaluation
4. **The CEO Next Door** - 4 CEO behaviors framework
5. **Power Score** - P × W × R executive effectiveness model

---

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  (React + TypeScript + Tailwind CSS)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTPS/REST
┌──────────────────▼──────────────────────────────────────────┐
│                API Gateway Layer                             │
│  (FastAPI + JWT Auth + RBAC)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Business Logic Layer                            │
│  ┌────────────┬────────────┬────────────┬────────────┐     │
│  │ Scorecard  │ Interview  │ Leadership │ Power      │     │
│  │ Service    │ Service    │ Service    │ Score      │     │
│  └────────────┴────────────┴────────────┴────────────┘     │
│  ┌────────────┬────────────┬────────────┐                  │
│  │ CEO        │ PDF Export │ Analytics  │                  │
│  │ Scorecard  │ Service    │ Service    │                  │
│  └────────────┴────────────┴────────────┘                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Data Access Layer                               │
│  (SQLAlchemy ORM + Alembic Migrations)                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│           PostgreSQL Database                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Module Breakdown

### 1. A-Method Scorecard Generator
**Purpose**: Create role-based scorecards defining mission, outcomes, and competencies

**Features**:
- Role mission definition
- 3-5 measurable outcomes with KPIs
- 5-8 competencies with behavioral anchors
- Version control and change history
- Team collaboration features
- Multi-format export (PDF, DOCX, JSON)

**Database Tables**:
- `scorecards`
- `scorecard_outcomes`
- `scorecard_competencies`
- `scorecard_versions`
- `scorecard_collaborators`

---

### 2. Structured Biographical Interview Generator
**Purpose**: Generate chronological interview scripts based on Topgrading methodology

**Features**:
- Career-by-career chronological interview wizard
- TORC (Threat of Reference Check) automation
- Achievement and failure pattern analysis
- Boss rating collection (1-10 scale)
- Reference check logic engine
- Red flag detection system
- Candidate Quality Index (CQI) scoring

**Database Tables**:
- `interviews`
- `interview_career_blocks`
- `interview_questions`
- `interview_responses`
- `boss_ratings`
- `reference_checks`
- `red_flags`

---

### 3. Leadership Assessor (CEO Next Door)
**Purpose**: Assess executives on the 4 CEO Behaviors

**The 4 Behaviors**:
1. **Decisiveness** - Speed, quality, cutting losses, handling ambiguity
2. **Reliability** - Delivering predictably, meeting commitments, process discipline
3. **Bold Adaptation** - Pivoting, recognizing inflection points, experimentation
4. **Engaging for Impact** - Stakeholder influence, alignment, vision, talent magnetism

**Features**:
- 360-degree assessment surveys
- Rater calibration tools
- Evidence-based behavior capture
- Individual development plans
- Executive dashboards

**Database Tables**:
- `leadership_assessments`
- `behavior_ratings`
- `raters`
- `evidence_items`
- `development_plans`

---

### 4. Power Score Engine
**Purpose**: Calculate and optimize executive effectiveness using P × W × R formula

**Formula**: **Power Score = Priorities (P) × Who (W) × Relationships (R)**

**Components**:
- **P (Priorities)**: Clarity, focus, alignment, resource consistency (0-10)
- **W (Who)**: Leadership bench strength, A-player ratio, team gaps (0-10)
- **R (Relationships)**: Board alignment, collaboration, trust, culture (0-10)

**Features**:
- Power Score calculation engine
- Weakest Link Detector
- Dimension-specific diagnostics
- Improvement roadmap generator
- Team effectiveness mapping

**Database Tables**:
- `power_scores`
- `priority_assessments`
- `who_assessments`
- `relationship_assessments`
- `improvement_plans`

---

### 5. CEO Scorecard Generator
**Purpose**: Comprehensive executive performance scorecard combining CEO Next Door + Power Score

**Components**:

#### A. CEO Next Door Behavioral Metrics
Each of the 4 behaviors broken into sub-dimensions (0-10 scale):
- Decisiveness: decision speed, decision quality, loss cutting, ambiguity handling
- Reliability: predictability, commitment delivery, process discipline, time management
- Bold Adaptation: pivot capacity, inflection recognition, experimentation, learning agility
- Engaging for Impact: stakeholder influence, alignment, vision communication, talent magnetism

#### B. Power Score Integration (P × W × R)
- Priorities scoring (clarity, focus, alignment, resources)
- Who scoring (bench strength, A-player ratio, gaps, delegation)
- Relationships scoring (board, collaboration, market, culture)

#### C. CEO Operating Metrics
- Quarterly goal achievement
- Revenue target performance
- Cash/runway discipline
- Strategy execution score
- People leadership score
- Org-wide engagement
- Customer impact score

**Outputs**:
- **CEO Excellence Index** (composite score 0-100)
- Full CEO scorecard report (PDF/DOCX)
- Leadership development recommendations
- Weakest behavior identification
- Weakest Power Score element
- Key leadership failure point diagnosis

**Database Tables**:
- `ceo_scorecards`
- `ceo_behavior_scores`
- `ceo_power_scores`
- `ceo_operating_metrics`
- `ceo_recommendations`

---

## Database Schema

### Core Entities

#### Users & Authentication
```sql
users
- id: UUID (PK)
- email: VARCHAR(255) UNIQUE
- hashed_password: VARCHAR(255)
- full_name: VARCHAR(255)
- role: ENUM('admin', 'board_member', 'founder', 'ceo', 'executive_coach', 'hr_manager')
- organization_id: UUID (FK)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- is_active: BOOLEAN
```

#### Organizations
```sql
organizations
- id: UUID (PK)
- name: VARCHAR(255)
- industry: VARCHAR(100)
- size: VARCHAR(50)
- created_at: TIMESTAMP
- subscription_tier: ENUM('free', 'professional', 'enterprise')
```

### Module-Specific Tables

#### A-Method Scorecards
```sql
scorecards
- id: UUID (PK)
- organization_id: UUID (FK)
- created_by: UUID (FK users)
- role_title: VARCHAR(255)
- role_mission: TEXT
- status: ENUM('draft', 'active', 'archived')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

scorecard_outcomes
- id: UUID (PK)
- scorecard_id: UUID (FK)
- description: TEXT
- metric: VARCHAR(255)
- target_value: VARCHAR(100)
- timeframe: VARCHAR(100)
- priority: INTEGER

scorecard_competencies
- id: UUID (PK)
- scorecard_id: UUID (FK)
- competency_name: VARCHAR(255)
- description: TEXT
- behavioral_anchors: JSONB
- weight: DECIMAL(3,2)
```

#### Topgrading Interviews
```sql
interviews
- id: UUID (PK)
- candidate_id: UUID (FK)
- interviewer_id: UUID (FK users)
- scorecard_id: UUID (FK)
- interview_date: TIMESTAMP
- status: ENUM('scheduled', 'in_progress', 'completed', 'cancelled')
- overall_rating: DECIMAL(3,2)
- cqi_score: INTEGER (0-100)
- recommendation: ENUM('strong_yes', 'yes', 'maybe', 'no', 'strong_no')

interview_career_blocks
- id: UUID (PK)
- interview_id: UUID (FK)
- company_name: VARCHAR(255)
- role_title: VARCHAR(255)
- start_date: DATE
- end_date: DATE
- achievements: JSONB
- failures: JSONB
- boss_name: VARCHAR(255)
- boss_rating: INTEGER (1-10)
- reason_for_leaving: TEXT

red_flags
- id: UUID (PK)
- interview_id: UUID (FK)
- flag_type: VARCHAR(100)
- severity: ENUM('low', 'medium', 'high', 'critical')
- description: TEXT
- detected_at: TIMESTAMP
```

#### Leadership Assessments
```sql
leadership_assessments
- id: UUID (PK)
- subject_id: UUID (FK users)
- assessment_period: VARCHAR(50)
- status: ENUM('pending', 'in_progress', 'completed')
- decisiveness_score: DECIMAL(4,2)
- reliability_score: DECIMAL(4,2)
- bold_adaptation_score: DECIMAL(4,2)
- engaging_impact_score: DECIMAL(4,2)
- overall_score: DECIMAL(4,2)
- created_at: TIMESTAMP

behavior_ratings
- id: UUID (PK)
- assessment_id: UUID (FK)
- rater_id: UUID (FK users)
- behavior_type: ENUM('decisiveness', 'reliability', 'bold_adaptation', 'engaging_impact')
- dimension: VARCHAR(100)
- score: INTEGER (0-10)
- evidence: TEXT
- submitted_at: TIMESTAMP
```

#### Power Scores
```sql
power_scores
- id: UUID (PK)
- executive_id: UUID (FK users)
- assessment_date: DATE
- priorities_score: DECIMAL(4,2)
- who_score: DECIMAL(4,2)
- relationships_score: DECIMAL(4,2)
- total_power_score: DECIMAL(8,2)
- weakest_dimension: VARCHAR(50)

priority_assessments
- id: UUID (PK)
- power_score_id: UUID (FK)
- clarity_score: INTEGER (0-10)
- focus_score: INTEGER (0-10)
- alignment_score: INTEGER (0-10)
- resource_consistency_score: INTEGER (0-10)
- notes: TEXT
```

#### CEO Scorecards
```sql
ceo_scorecards
- id: UUID (PK)
- ceo_id: UUID (FK users)
- organization_id: UUID (FK)
- period: VARCHAR(50) (e.g., 'Q1 2025')
- ceo_excellence_index: DECIMAL(5,2) (0-100)
- status: ENUM('draft', 'finalized', 'archived')
- created_at: TIMESTAMP
- finalized_at: TIMESTAMP

ceo_behavior_scores
- id: UUID (PK)
- ceo_scorecard_id: UUID (FK)
- behavior_type: ENUM('decisiveness', 'reliability', 'bold_adaptation', 'engaging_impact')
- decision_speed: INTEGER (0-10)
- decision_quality: INTEGER (0-10)
- loss_cutting: INTEGER (0-10)
- ambiguity_handling: INTEGER (0-10)
- predictability: INTEGER (0-10)
- commitment_delivery: INTEGER (0-10)
- process_discipline: INTEGER (0-10)
- time_management: INTEGER (0-10)
- pivot_capacity: INTEGER (0-10)
- inflection_recognition: INTEGER (0-10)
- experimentation_velocity: INTEGER (0-10)
- learning_agility: INTEGER (0-10)
- stakeholder_influence: INTEGER (0-10)
- cross_functional_alignment: INTEGER (0-10)
- vision_communication: INTEGER (0-10)
- talent_magnetism: INTEGER (0-10)
- overall_behavior_score: DECIMAL(4,2)

ceo_operating_metrics
- id: UUID (PK)
- ceo_scorecard_id: UUID (FK)
- quarterly_goal_achievement: INTEGER (0-100)
- revenue_target_performance: INTEGER (0-100)
- cash_runway_discipline: INTEGER (0-100)
- strategy_execution_score: INTEGER (0-100)
- people_leadership_score: INTEGER (0-100)
- org_engagement_score: INTEGER (0-100)
- customer_impact_score: INTEGER (0-100)

ceo_recommendations
- id: UUID (PK)
- ceo_scorecard_id: UUID (FK)
- recommendation_type: ENUM('behavior_improvement', 'power_score_improvement', 'failure_point_mitigation')
- priority: ENUM('critical', 'high', 'medium', 'low')
- title: VARCHAR(255)
- description: TEXT
- action_items: JSONB
- expected_impact: TEXT
```

---

## API Structure

### Authentication & Users
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile

### Scorecards (A-Method)
- `GET /api/v1/scorecards` - List all scorecards
- `POST /api/v1/scorecards` - Create scorecard
- `GET /api/v1/scorecards/{id}` - Get scorecard
- `PUT /api/v1/scorecards/{id}` - Update scorecard
- `DELETE /api/v1/scorecards/{id}` - Delete scorecard
- `POST /api/v1/scorecards/{id}/outcomes` - Add outcome
- `POST /api/v1/scorecards/{id}/competencies` - Add competency
- `GET /api/v1/scorecards/{id}/export/pdf` - Export PDF
- `GET /api/v1/scorecards/{id}/export/docx` - Export DOCX

### Interviews (Topgrading)
- `GET /api/v1/interviews` - List interviews
- `POST /api/v1/interviews` - Create interview
- `GET /api/v1/interviews/{id}` - Get interview
- `PUT /api/v1/interviews/{id}` - Update interview
- `POST /api/v1/interviews/{id}/career-blocks` - Add career block
- `POST /api/v1/interviews/{id}/calculate-cqi` - Calculate CQI
- `GET /api/v1/interviews/{id}/red-flags` - Get red flags
- `GET /api/v1/interviews/{id}/export/pdf` - Export report

### Leadership Assessments
- `GET /api/v1/leadership/assessments` - List assessments
- `POST /api/v1/leadership/assessments` - Create assessment
- `GET /api/v1/leadership/assessments/{id}` - Get assessment
- `POST /api/v1/leadership/assessments/{id}/ratings` - Submit ratings
- `GET /api/v1/leadership/assessments/{id}/dashboard` - Get dashboard

### Power Scores
- `GET /api/v1/power-scores` - List power scores
- `POST /api/v1/power-scores` - Create power score
- `GET /api/v1/power-scores/{id}` - Get power score
- `PUT /api/v1/power-scores/{id}` - Update power score
- `POST /api/v1/power-scores/{id}/calculate` - Calculate score
- `GET /api/v1/power-scores/{id}/weakest-link` - Identify weakest link
- `GET /api/v1/power-scores/{id}/improvement-plan` - Generate plan

### CEO Scorecards
- `GET /api/v1/ceo-scorecards` - List CEO scorecards
- `POST /api/v1/ceo-scorecards` - Create CEO scorecard
- `GET /api/v1/ceo-scorecards/{id}` - Get CEO scorecard
- `PUT /api/v1/ceo-scorecards/{id}` - Update CEO scorecard
- `POST /api/v1/ceo-scorecards/{id}/finalize` - Finalize scorecard
- `GET /api/v1/ceo-scorecards/{id}/excellence-index` - Get excellence index
- `GET /api/v1/ceo-scorecards/{id}/recommendations` - Get recommendations
- `GET /api/v1/ceo-scorecards/{id}/export/pdf` - Export full report

---

## Frontend Structure

```
src/
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Layout.tsx
│   ├── scorecards/
│   │   ├── ScorecardForm.tsx
│   │   ├── ScorecardList.tsx
│   │   └── ScorecardViewer.tsx
│   ├── interviews/
│   │   ├── InterviewWizard.tsx
│   │   ├── CareerBlockForm.tsx
│   │   └── RedFlagPanel.tsx
│   ├── leadership/
│   │   ├── BehaviorRatingForm.tsx
│   │   ├── AssessmentDashboard.tsx
│   │   └── DevelopmentPlan.tsx
│   ├── power-score/
│   │   ├── PowerScoreCalculator.tsx
│   │   ├── DimensionAssessment.tsx
│   │   └── ImprovementRoadmap.tsx
│   └── ceo-scorecard/
│       ├── CEOScorecardForm.tsx
│       ├── BehaviorScoreInput.tsx
│       ├── OperatingMetricsInput.tsx
│       ├── ExcellenceIndexDisplay.tsx
│       └── RecommendationsPanel.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── Login.tsx
│   ├── Scorecards.tsx
│   ├── Interviews.tsx
│   ├── LeadershipAssessments.tsx
│   ├── PowerScores.tsx
│   └── CEOScorecards.tsx
├── services/
│   ├── api.ts
│   ├── auth.ts
│   └── export.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useScorecards.ts
│   └── useCEOScorecard.ts
├── types/
│   └── index.ts
└── App.tsx
```

---

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL 15+
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib + bcrypt
- **PDF Generation**: ReportLab / WeasyPrint
- **DOCX Generation**: python-docx
- **Testing**: Pytest + pytest-asyncio

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **State Management**: React Context + Hooks
- **HTTP Client**: Axios
- **Routing**: React Router 6+
- **Forms**: React Hook Form
- **PDF Viewer**: react-pdf
- **Testing**: React Testing Library + Jest

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

---

## Security

### Authentication
- JWT-based authentication with access and refresh tokens
- Access token expiry: 30 minutes
- Refresh token expiry: 7 days
- Secure HTTP-only cookies for refresh tokens

### Authorization (RBAC)
**Roles**:
- `admin` - Full system access
- `board_member` - View CEO scorecards, leadership assessments
- `founder` - Full organizational access
- `ceo` - View own assessments, create scorecards for team
- `executive_coach` - Create assessments, view assigned clients
- `hr_manager` - Create scorecards, interviews, assessments

**Permissions Matrix**:
| Resource | Admin | Board | Founder | CEO | Coach | HR |
|----------|-------|-------|---------|-----|-------|-----|
| Scorecards | CRUD | R | CRUD | CRU | CRU | CRUD |
| Interviews | CRUD | R | CRUD | CR | CR | CRUD |
| Leadership | CRUD | R | CRUD | R | CRUD | CRU |
| Power Score | CRUD | R | CRUD | R | CRU | CRU |
| CEO Scorecard | CRUD | R | CRUD | R | CRU | CRU |

---

## Deployment

### Docker Compose (Development)
```yaml
services:
  - postgres (database)
  - backend (FastAPI)
  - frontend (React dev server)
  - nginx (reverse proxy)
```

### Kubernetes (Production)
```
Deployments:
  - postgres-deployment
  - backend-deployment (3 replicas)
  - frontend-deployment (3 replicas)

Services:
  - postgres-service (ClusterIP)
  - backend-service (ClusterIP)
  - frontend-service (LoadBalancer)

ConfigMaps:
  - backend-config
  - frontend-config

Secrets:
  - postgres-secret
  - jwt-secret
```

---

## Performance Targets

- API response time: < 200ms (p95)
- Page load time: < 2s (p95)
- Concurrent users: 10,000+
- Database queries: < 50ms (p95)
- PDF generation: < 3s
- Uptime: 99.9%

---

## Next Steps
1. Implement database models
2. Build API endpoints
3. Create frontend components
4. Add authentication
5. Implement business logic
6. Create tests
7. Setup CI/CD
8. Deploy to production
