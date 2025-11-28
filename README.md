# A-Player Hiring Suite

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

**Comprehensive hiring and leadership assessment platform integrating five premier frameworks**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📋 Overview

The **A-Player Hiring Suite** is a production-ready SaaS platform that integrates five evidence-based hiring and leadership frameworks into a unified system:

1. **Who: The A Method for Hiring** - Scorecard-based hiring methodology
2. **Topgrading** - Chronological in-depth structured interviews
3. **Foolproof Hiring** - Evidence-based candidate evaluation
4. **The CEO Next Door** - 4 CEO behaviors framework
5. **Power Score** - Executive effectiveness formula (P × W × R)

This suite enables organizations to:
- Create role scorecards with clear missions and outcomes
- Conduct structured interviews with TORC methodology
- Assess executives on the 4 CEO behaviors
- Calculate executive effectiveness using Power Score
- Generate comprehensive CEO performance scorecards

---

## ✨ Features

### 1. A-Method Scorecard Generator (WHO)
- **Role Definition**: Clear mission statements for each position
- **Measurable Outcomes**: 3-5 quantifiable success metrics
- **Key Competencies**: 5-8 critical skills with behavioral anchors
- **Collaboration**: Team-based scorecard development
- **Version Control**: Track changes over time
- **Export**: PDF, DOCX, JSON formats

### 2. Topgrading Interview System
- **Chronological Wizard**: Career-by-career interview structure
- **TORC Automation**: Threat of Reference Check methodology
- **Pattern Analysis**: Automatic detection of achievement/failure patterns
- **Boss Ratings**: 1-10 scale predictions
- **Red Flag Detection**: Automatic warning system
- **CQI Scoring**: Candidate Quality Index (0-100)
- **Reference Logic**: Intelligent reference check routing

### 3. Leadership Assessor (CEO Next Door)
Assess executives on **The 4 CEO Behaviors**:

#### 1. Decisiveness
- Decision speed
- Decision quality
- Ability to cut losses
- Handling ambiguity

#### 2. Reliability
- Delivering predictably
- Meeting commitments
- Process discipline
- Time management

#### 3. Bold Adaptation
- Pivoting under pressure
- Recognizing inflection points
- Experimentation velocity
- Learning agility

#### 4. Engaging for Impact
- Stakeholder influence
- Cross-functional alignment
- Vision communication
- Talent magnetism

**Features**:
- 360-degree assessment surveys
- Rater calibration tools
- Evidence capture system
- Individual development plans
- Executive dashboards

### 4. Power Score Engine
**Formula**: `Power Score = P × W × R`

#### P - Priorities (0-10)
- Clarity of priorities
- Focus maintenance
- Team alignment
- Resource consistency

#### W - Who (0-10)
- Leadership bench strength
- A-player ratio
- Team gap assessment
- Delegation efficiency

#### R - Relationships (0-10)
- Board alignment
- Cross-team collaboration
- Market trust
- Culture health

**Features**:
- Weakest Link Detector
- Dimension diagnostics
- Improvement roadmap generator
- Team effectiveness mapping

### 5. CEO Scorecard Generator ⭐
**Comprehensive executive performance assessment combining all frameworks**

#### Components:

**A. CEO Next Door Behavioral Metrics**
- All 4 behaviors with sub-dimensions (16 total metrics)
- Each scored 0-10
- Weakest/strongest behavior identification

**B. Power Score Integration**
- Full P × W × R assessment
- 12 sub-components
- Total Power Score calculation

**C. CEO Operating Metrics**
- Quarterly goal achievement
- Revenue target performance
- Cash/runway discipline
- Strategy execution score
- People leadership score
- Org-wide engagement
- Customer impact score

**Outputs**:
- **CEO Excellence Index** (0-100 composite score)
- Full scorecard report (PDF/DOCX)
- Development recommendations by priority
- Weakest behavior identification
- Weakest Power Score element
- Key leadership failure point diagnosis

**Access Control**:
- Board members
- Founders
- CEOs (view own)
- Executive coaches
- HR managers

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL 15+
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib + bcrypt
- **Testing**: Pytest + pytest-asyncio

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3+
- **State Management**: React Query + Hooks
- **HTTP Client**: Axios
- **Routing**: React Router 6+
- **Forms**: React Hook Form
- **Icons**: Lucide React

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL with persistent volumes

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OR: Python 3.11+, Node.js 18+, PostgreSQL 15+

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd A_Player_Hiring_Suite

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
echo "VITE_API_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

#### Database Setup

```bash
# Create PostgreSQL database
createdb aplayer_hiring

# Or using psql
psql -U postgres
CREATE DATABASE aplayer_hiring;
CREATE USER aplayer WITH PASSWORD 'aplayer123';
GRANT ALL PRIVILEGES ON DATABASE aplayer_hiring TO aplayer;
```

---

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/v1/auth/register    - Register new user
POST /api/v1/auth/login       - Login
POST /api/v1/auth/refresh     - Refresh token
GET  /api/v1/auth/me          - Get current user
```

### Scorecard Endpoints
```
GET    /api/v1/scorecards           - List scorecards
POST   /api/v1/scorecards           - Create scorecard
GET    /api/v1/scorecards/{id}      - Get scorecard
PUT    /api/v1/scorecards/{id}      - Update scorecard
DELETE /api/v1/scorecards/{id}      - Delete scorecard
POST   /api/v1/scorecards/{id}/outcomes     - Add outcome
POST   /api/v1/scorecards/{id}/competencies - Add competency
```

### Interview Endpoints
```
GET  /api/v1/interviews            - List interviews
POST /api/v1/interviews            - Create interview
GET  /api/v1/interviews/{id}       - Get interview
GET  /api/v1/interviews/{id}/red-flags - Get red flags
```

### Leadership Assessment Endpoints
```
GET  /api/v1/leadership/assessments     - List assessments
POST /api/v1/leadership/assessments     - Create assessment
GET  /api/v1/leadership/assessments/{id} - Get assessment
```

### Power Score Endpoints
```
GET  /api/v1/power-scores                    - List power scores
POST /api/v1/power-scores                    - Create power score
GET  /api/v1/power-scores/{id}               - Get power score
GET  /api/v1/power-scores/{id}/weakest-link  - Get weakest link
```

### CEO Scorecard Endpoints ⭐
```
GET  /api/v1/ceo-scorecards                        - List CEO scorecards
POST /api/v1/ceo-scorecards                        - Create CEO scorecard
GET  /api/v1/ceo-scorecards/{id}                   - Get CEO scorecard
PUT  /api/v1/ceo-scorecards/{id}                   - Update CEO scorecard
POST /api/v1/ceo-scorecards/{id}/finalize          - Finalize scorecard
GET  /api/v1/ceo-scorecards/{id}/excellence-index  - Get excellence index
GET  /api/v1/ceo-scorecards/{id}/recommendations   - Get recommendations
```

**Interactive API Documentation**: Visit `http://localhost:8000/api/v1/docs` when running the backend.

---

## 🔐 Security & Authentication

### JWT-Based Authentication
- **Access Token**: 30 minutes expiry
- **Refresh Token**: 7 days expiry
- **Algorithm**: HS256
- **Secure Storage**: HTTP-only cookies recommended

### Role-Based Access Control (RBAC)

| Role | Permissions |
|------|------------|
| **Admin** | Full system access |
| **Board Member** | View CEO scorecards, leadership assessments |
| **Founder** | Full organizational access |
| **CEO** | View own assessments, create team scorecards |
| **Executive Coach** | Create assessments, view assigned clients |
| **HR Manager** | Create scorecards, interviews, assessments |

---

## 🗄 Database Schema

### Core Tables
- `users` - User accounts and authentication
- `organizations` - Company/organization data
- `scorecards` - A-Method role scorecards
- `scorecard_outcomes` - Measurable outcomes
- `scorecard_competencies` - Key competencies
- `interviews` - Topgrading interviews
- `interview_career_blocks` - Career history segments
- `red_flags` - Interview warning indicators
- `leadership_assessments` - CEO behavior assessments
- `behavior_ratings` - 360-degree ratings
- `power_scores` - P × W × R assessments
- `ceo_scorecards` - Comprehensive CEO scorecards
- `ceo_behavior_scores` - CEO behavior metrics
- `ceo_power_scores` - CEO Power Score metrics
- `ceo_operating_metrics` - CEO operating performance
- `ceo_recommendations` - Development recommendations

For detailed schema, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## 🐳 Deployment

### Docker Compose (Development/Staging)

```bash
# Build and start
docker-compose up --build -d

# Scale backend
docker-compose up --scale backend=3 -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Kubernetes (Production)

```bash
# Apply PostgreSQL deployment
kubectl apply -f kubernetes/postgres-deployment.yaml

# Apply backend deployment
kubectl apply -f kubernetes/backend-deployment.yaml

# Apply frontend deployment
kubectl apply -f kubernetes/frontend-deployment.yaml

# Check deployments
kubectl get deployments
kubectl get pods
kubectl get services

# Scale backend
kubectl scale deployment backend-deployment --replicas=5

# View logs
kubectl logs -f deployment/backend-deployment
```

### Environment Variables

**Backend (`.env`)**:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key-min-32-characters
DEBUG=false
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

**Frontend**:
```env
VITE_API_URL=https://api.yourdomain.com
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
pytest -v tests/test_ceo_scorecard.py
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

---

## 📊 Performance Targets

- **API Response Time**: < 200ms (p95)
- **Page Load Time**: < 2s (p95)
- **Concurrent Users**: 10,000+
- **Database Queries**: < 50ms (p95)
- **PDF Generation**: < 3s
- **Uptime**: 99.9%

---

## 📖 Framework References

### Books & Methodologies
1. **Who: The A Method for Hiring** - Geoff Smart & Randy Street
2. **Topgrading** - Bradford D. Smart
3. **Foolproof Hiring** - Bradford D. Smart
4. **The CEO Next Door** - Elena L. Botelho & Kim R. Powell
5. **Power Score** - Effective executive assessment

### Research Foundations
- 10-year CEO Genome Project
- 17,000+ executive assessments
- Evidence-based hiring science
- Predictive validity research

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- **Backend**: PEP 8, type hints, docstrings
- **Frontend**: ESLint, Prettier, TypeScript strict mode
- **Tests**: Minimum 80% coverage

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Geoff Smart & Randy Street (Who: The A Method)
- Bradford D. Smart (Topgrading)
- Elena L. Botelho & Kim R. Powell (The CEO Next Door)
- ghSMART & Company (CEO Genome Project)

---

## 📧 Support

For support, questions, or feature requests:
- **Issues**: [GitHub Issues](https://github.com/yourusername/a-player-hiring-suite/issues)
- **Email**: support@aplayer-hiring-suite.com
- **Documentation**: [Full Documentation](docs/)

---

## 🗺 Roadmap

### Version 1.1 (Planned)
- [ ] Advanced analytics dashboards
- [ ] Machine learning candidate predictions
- [ ] Mobile applications (iOS/Android)
- [ ] Slack/Teams integrations
- [ ] Advanced PDF templates
- [ ] Multi-language support

### Version 1.2 (Planned)
- [ ] Video interview integration
- [ ] AI-powered interview question generation
- [ ] Automated reference check scheduling
- [ ] Custom workflow builder
- [ ] Advanced reporting engine

---

<div align="center">

**Built with ❤️ using FastAPI, React, and evidence-based hiring science**

[⬆ Back to Top](#a-player-hiring-suite)

</div>
