# 🌏 Project CT - Smart Tourism System

An AI-powered travel **chatbot** that processes user queries to provide information about **Vietnamese tourist** destinations, local cuisines, and real-time weather updates.

---

## 👥 Team Members

| No. | Name            | Role         |
|-----|------------------|--------------|
| 1   | Nguyen Nam (*)   | Team Leader  |
| 2   | Hong Truc (*)    | Member       |
| 3   | Minh Khang (*)   | Member       |
| 4   | Tony Dang (*)    | Member       |
| 5   | Quoc Huy (*)     | Member       |
| 6   | Trung Hien (*)   | Member       |
| 7   | Thi Anh (*)      | Member       |

> (*) IT - University of Science - VNU

---

# 🚀 How-to Guide

## 1. Create a Gemini API Key

If you don’t have a **Google AI Studio** account yet, create one at:  
👉 https://aistudio.google.com  

Then follow these steps:

1. Go to **[Google AI Studio API Keys](https://aistudio.google.com/apikey)**  
2. Click **“Create API Key”**  
3. Select an existing project (or create a new one)  
4. Copy the generated API key  

> ⚠️ **Note:** Keep this key private — never share or upload your `.env` file.

---

## 2. Create an OpenWeather API Key

To enable **real-time weather information**, you need an API key from **OpenWeather**.

Follow these steps:

1. Go to **[OpenWeather API](https://openweathermap.org/api)**  
2. Click **“Sign up”** (if you don’t already have an account)  
3. After logging in, navigate to:  
   👉 [My API Keys](https://home.openweathermap.org/api_keys)
4. Click **“Create Key”** and give it a name (e.g., `smart-tourism-weather`)  
5. Copy the generated key (it looks like a long string of letters/numbers)

---

## 3. Add API Keys to Environment File

Inside your `backend/` folder, create a `.env` file (if it doesn’t already exist) and add your keys:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

> ⚠️ **Do not share or commit this file.**  
> Always keep your API keys private and secure.

---

## 4. Run the API Locally

Move into the backend folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the development server:
```bash
uvicorn app.api.main:app --reload
```

Open your browser and visit Swagger UI for API documentation:  
👉 http://localhost:8000/docs

---

# 🌿 Git Feature Branch Workflow

We use **Feature Branch Workflow** for clean, collaborative development.

## Branch Naming Convention

| Branch Type | Description | Example |
|--------------|-------------|----------|
| `main` | Stable production-ready code | — |
| `feature/<feature-name>` | New feature branches | `feature/add-weather-api` |
| `bugfix/<description>` | Small fixes | `bugfix/fix-response-parser` |
| `hotfix/<description>` | Urgent production fixes | `hotfix/api-crash` |

---

## Workflow Steps

### 1️⃣ Start a New Feature
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 2️⃣ Work on the Feature
```bash
git add .
git commit -m "feat: short and clear message"
```

### 3️⃣ Push and Create Pull Request
```bash
git push -u origin feature/your-feature-name
```

Then open a Pull Request on GitHub and request code review from your teammates.

---

## ✅ Example `.env` File (Final)
```bash
GOOGLE_API_KEY=AIzaSyBxxxxxx...
OPENWEATHER_API_KEY=7026d46ce34xxxxxx...
```

> 📌 This enables both:
> - **Gemini API** → AI chatbot responses  
> - **OpenWeather API** → Real-time weather updates for destinations
