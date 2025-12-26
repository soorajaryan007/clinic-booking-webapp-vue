
## 🏥 Clinic Scheduler

### Full-Stack Appointment Booking System

A modern, production-ready appointment scheduling platform built with **Vue 3**, **FastAPI**, **SQLite**, and the **Cal.com API**.

The system allows users to browse event types, select dates and time slots, verify their email via OTP, and confirm appointments.
All bookings are **persisted locally** and **synchronized with Cal.com in real time**.

---

## ✨ Features

* 🔄 Dynamic event type fetching from **Cal.com**
* ⏱️ Automatic generation of available time slots
* 📧 **Email OTP verification** before booking
* 📅 Book, reschedule, and cancel appointments
* 💾 Local persistence using **SQLite**
* 🔗 Real-time synchronization with **Cal.com**
* 📱 Responsive **Vue 3 + Vite** frontend
* ⚙️ Clean, modular **FastAPI** backend
* 🐳 **Dockerized** for one-command startup
* 📘 Clear, developer-friendly documentation

---

## 🏗️ Project Architecture

```
calbookingwebapp/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── cal.py
│   │   ├── slot_engine.py
│   │   ├── database.py
│   │   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env            # Not committed (Cal API key)
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
└── docker-compose.yml
```

---

## 🐳 Run with Docker (Recommended)

Running the entire stack via Docker is the **fastest and easiest** option.
No need to install Python, Node.js, pip, or npm locally.

---

### 1️⃣ Prerequisites

Ensure Docker is installed:

```bash
docker --version
docker compose version
```

---

### 2️⃣ Create Backend Environment File

Create the following file:

```
backend/.env
```

Add your Cal.com API key:

```env
CAL_API_KEY=cal_live_xxxxxxxxxxxxxxxxxxxx
```

> ⚠️ This file is ignored by Git and **must exist before building containers**.

---

### 3️⃣ Start the Full Stack

From the project root:

```bash
docker compose up --build
```

Docker will:

* ✅ Build the backend image
* ✅ Build the Vue frontend image
* ✅ Create a shared Docker network
* ✅ Start all services

---

### 4️⃣ Access the Application

| Service            | URL                                                      |
| ------------------ | -------------------------------------------------------- |
| Frontend (Vue)     | [http://localhost:5173](http://localhost:5173)           |
| Backend (FastAPI)  | [http://localhost:8000](http://localhost:8000)           |
| API Docs (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |

---

### 5️⃣ Stop Containers

```bash
docker compose down
```

---

### 6️⃣ Rebuild Cleanly

```bash
docker compose build --no-cache
docker compose up
```

---

## ⚙️ Manual Local Setup (Optional)

If you prefer not to use Docker, you can run the backend and frontend separately.

---

## 🔧 Backend Setup (FastAPI)

### 1️⃣ Navigate to backend

```bash
cd backend
```

### 2️⃣ Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env`

```env
CAL_API_KEY=cal_live_xxxxxxxxx
```

### 5️⃣ Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:

```
http://localhost:8000
http://localhost:8000/docs
```

---

## 🖥️ Frontend Setup (Vue 3 + Vite)

### 1️⃣ Navigate to frontend

```bash
cd frontend
```

### 2️⃣ Install dependencies

> ⚠️ Requires **Node.js 18+** (recommended: Node 20)

```bash
npm install
```

### 3️⃣ Start development server

```bash
npm run dev
```

Open in browser:

```
http://localhost:5173
```

---

## 🔑 Cal.com API Setup

1. Visit:
   [https://app.cal.com/settings/developer](https://app.cal.com/settings/developer)
2. Create a **Personal Access Token**
3. Copy the token
4. Add it to `backend/.env`:

```env
CAL_API_KEY=cal_live_xxxxxxx
```

5. Ensure event types exist:
   [https://app.cal.com/event-types](https://app.cal.com/event-types)
6. Event duration **must match slot engine logic**
   (e.g., a 15-minute event must produce 15-minute slots)

---

## 🔄 Booking Workflow

1. Vue frontend loads event types from the backend
2. User selects an event type and date
3. Backend generates available time slots
4. User selects a slot and enters **name + email**
5. Email OTP verification is performed
6. Backend:

   * Saves booking in SQLite
   * Syncs appointment with Cal.com
7. Vue UI shows booking confirmation
8. User can **reschedule or cancel** the appointment

---

## 🧪 Debugging & Logs

### Docker logs

```bash
docker logs clinic-backend
```

### Manual run logs

```bash
uvicorn app.main:app --reload
```

---

## 📁 .gitignore

Sensitive and generated files are excluded:

```
backend/.env
backend/venv/
backend/__pycache__/
frontend/node_modules/
*.log
```

---

## ✅ Project Status

* ✔ Vue 3 frontend (Vite)
* ✔ FastAPI backend
* ✔ Cal.com integration
* ✔ Email OTP verification
* ✔ Booking / reschedule / cancel flows
* ✔ Fully Dockerized

---

