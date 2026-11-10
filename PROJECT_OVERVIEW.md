# Smart District Administration Dashboard - Project Overview

## 1. Executive Summary

**Smart District Administration** is a centralized municipal and district management dashboard application designed for district administrators, department heads, and operational staff. Originally conceptualized and prototyped as a Streamlit application, it has been modernized into a decoupled, production-ready full-stack architecture powered by a **FastAPI** backend and a **React.js** frontend with **Ant Design**.

The platform streamlines:
- Cross-departmental coordination and communication.
- Real-time operational metric and KPI tracking.
- Task assignment, progress monitoring, and priority escalations.
- Budget allocation, resource utilization, and predictive forecasting.
- Geospatial mapping and administrative infrastructure oversight.

---

## 2. Architecture & Technology Stack

### Full-Stack Architecture Diagram

```
┌────────────────────────────────────────────────────────┐
│                   React 19 Frontend                    │
│   (Ant Design v5, React Router v7, Recharts, Leaflet)   │
│                 http://localhost:3000                  │
└───────────────────────────┬────────────────────────────┘
                            │
               HTTP / REST API (JWT Bearer)
             (Proxy configured via setupProxy)
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   FastAPI Backend                      │
│        (Uvicorn ASGI Server, PyJWT, Bcrypt)            │
│                 http://localhost:8000                  │
└───────────────────────────┬────────────────────────────┘
                            │
              Optional Relational Database
                            ▼
┌────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                  │
│       (Configured via DATABASE_URL in .env)            │
│   * In-memory mock store enabled for local dev/testing  │
└────────────────────────────────────────────────────────┘
```

### Technology Matrix

| Layer | Technologies & Libraries | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | React 19, Ant Design (`antd` v5), `@ant-design/icons` | Component design system, modals, forms, tables, layouts |
| **Frontend Routing & Auth** | `react-router-dom` v7, Context API (`AuthContext`) | Role-based protected routes and JWT session management |
| **Data Visualization** | `recharts`, `plotly.js`, `react-plotly.js` | Performance trend charts, resource distributions, predictions |
| **Mapping & GIS** | `leaflet`, `react-leaflet` | Geospatial visualization of district assets and facilities |
| **Backend API** | FastAPI, Uvicorn, Pydantic v2 | High-performance asynchronous REST API |
| **Security & Auth** | PyJWT (`HS256`), Bcrypt, HTTPBearer | Token generation, validation, and hashed credential checks |
| **Data Storage** | PostgreSQL, SQLAlchemy (or in-memory mock store) | User records, task persistence, metrics, and audit logs |

---

## 3. Directory Structure

```
Smart-District-Administration/
├── backend/
│   └── main.py                     # FastAPI application entrypoint & REST API endpoints
├── public/                         # React static assets & index.html template
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   └── ProtectedRoute.js   # Route guard enforcing authentication
│   │   ├── Common/
│   │   │   └── ErrorBoundary.js    # Global React error boundary handler
│   │   └── Layout/
│   │       └── Layout.js           # Responsive app frame with header, sidebar, and nav
│   ├── contexts/
│   │   └── AuthContext.js          # Authentication state, login/logout, and user context
│   ├── pages/
│   │   ├── Dashboard.js            # Role-specific KPI dashboards
│   │   ├── DepartmentCoordination.js # Cross-department workflows & meetings
│   │   ├── GeospatialView.js       # Interactive district GIS maps
│   │   ├── Login.js                # Multi-role login view with demo autofill
│   │   ├── PerformanceMetrics.js   # In-depth departmental analytics
│   │   ├── PredictiveAnalytics.js  # AI/ML-driven resource & budget forecasting
│   │   ├── Reports.js              # Scheduled & downloadable reports
│   │   ├── ResourceManagement.js   # Budget and equipment tracking
│   │   └── TaskTracking.js         # Kanban / task list tracking
│   ├── services/
│   │   ├── api.js                  # Axios client with interceptors
│   │   └── authService.js          # Authentication service calls
│   ├── App.js                      # Root router and theme config provider
│   ├── index.js                    # React DOM root mounting
│   └── setupProxy.js               # Dev proxy routing /api requests to port 8000
├── .env.example                    # Environment template
├── package.json                    # Node.js dependencies and scripts
└── pyproject.toml                  # Python package specifications
```

---

## 4. Key Functional Modules

### 1. Role-Based Access Control (RBAC)
- **Administrator**: Comprehensive district oversight including all departments, total budget utilization, city-wide staff counts, and high-level KPI trends.
- **Department Head**: Departmental metrics, team member workload, completion rates, and project coordination.
- **Staff Member**: Daily tasks, personal deliverables, deadlines, and weekly completion statistics.

### 2. Operational Dashboards
- Tailored KPI metric cards with change indicators (`+12.5%`, `+8.3%`).
- Department filters to inspect individual operational units (Public Works, Health, Education, Transportation, Finance, IT, etc.).

### 3. Task Management & Tracking
- Priority tags (`Low`, `Medium`, `High`, `Critical`).
- Real-time status workflow (`Pending`, `In Progress`, `Completed`, `Cancelled`).
- Department tagging and due-date tracking.

### 4. Advanced Analytics & GIS Mapping
- Resource allocation breakdown and budget utilization tracking.
- Leaflet-based mapping for district infrastructure, facilities, and service requests.
- Trend analysis and forecasting models for municipal service demands.

---

## 5. Running the Application

### Prerequisites
- Node.js (v18+)
- Python (v3.11+ / v3.13 tested)

### Starting the Services

#### 1. Backend API (FastAPI)
```powershell
# From the project root
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- Available at: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`
- Alternative ReDoc: `http://localhost:8000/redoc`

#### 2. Frontend Development Server (React)
```powershell
# From the project root
npm start
```
- Available at: `http://localhost:3000`

---

## 6. Demo Accounts & Credentials

The application includes pre-configured mock credentials for testing role-specific features:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full district administration, multi-department oversight |
| **Department Head** | `dept_head` | `dept123` | Department management (Public Works), team allocation |
| **Staff Member** | `staff` | `staff123` | Individual task execution and personal metrics |

