# Project CT - Smart Tourism System

An AI-powered travel **chatbot** that processes user text queries to provide information about **Vietnamese tourist** destinations and their local cuisines.

## Team Members

| No. | Name                     | Role            |
|-----|--------------------------|------------------|
| 1   | Nguyen Nam      (*)     | Team Leader     |    
| 2   | Hong Truc         (*)        | Member          |
| 3   | Minh Khang         (*)       | Member          |
| 4   | Tony Dang         (*)        | Member          |
| 5   | Quoc Huy         (*)         | Member          |
| 6   | Trung Hien       (*)         | Member          |
| 7   | Thi Anh          (*)         | Member          |

(*): IT - University of Science - VNU

# How-to Guide

## 1. Create a Gemini API Key
If you don’t have a Google AI Studio account yet, please create one at:
https://aistudio.google.com

Then follow these steps:

- Go to https://aistudio.google.com/apikey

- Click **Create API Key**

- Select a project (or create a new one)

- Copy the generated API key

## 2. Add API Key to environment file
Inside the `backend/` folder, create a `.env` file and add your API key:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```
Never share or upload your API key. Keep the .env file private.

## 3. Run the API locally
```bash
cd backend 
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the server:
```bash
uvicorn app.api.main:app --reload
```
Open your browser to access API documentation (Swagger UI): http://localhost:8000/docs

# Git Feature Branch Workflow

We use **Feature Branch Workflow** to manage collaborative development efficiently.

## Branch Naming Convention

- `main`: Stable production-ready code
- `feature/<feature-name>`: New feature branches  

  > Example: `feature/hold-mechanic`, `feature/add-menu`

- `bugfix/<description>`: For small fixes  

  > Example: `bugfix/ghost-piece`

- `hotfix/<description>`: Urgent production fixes

## Workflow Steps
1. **Start a Feature**
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```
2. **Work on the Feature**
```bash
git add .
git commit -m "feat: short and clear message"
```
3. **Push and Create Pull Request**
```bash
git push -u origin feature/your-feature-name
```