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