```bash
smart-tourism-system/
├── backend/                         # Python backend (FastAPI + AI agents)
│   ├── .env                         # TODO: Thêm API_KEYS (Gemini)
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── agents/                  # TODO: Chứa logic AI/Langchain/LlamaIndex
│       │   └── TODO:
│       │       - Implement LLM wrapper (Gemini/DeepSeek)
│       │       - Add Travel QA Agent (tourism info)
│       │       - Add Food Suggestion Agent
│       │       - Add Web Search Agent (optional)
│       │
│       ├── api/
│       │   ├── main.py              # TODO: tạo FastAPI app, router, root health check
│       │   ├── utils.py             # TODO: helper functions: format_response, sanitize_input
│       │   
│       │
│       ├── services/
│       │   └── TODO:
│       │       - Travel info service (get location descriptions)
│       │       - Food recommendation service
│       │       - Optional: External API connectors (Google Maps)
│       │
│       └── models/ (optional)
│           └── TODO:
│               - Request/Response Pydantic schemas for API
│               - Chat message model
│
├── frontend/                        # TODO: Web UI (HTML/CSS/JS or React)
│   └── TODO:
│       - Design layout for chatbot UI
│       - Connect backend API (/ask endpoint)
│       - Build simple chat interface
│
├── scripts/                         # Automation scripts
│   └── TODO:
│       - Script seed tourism data
│       - Script process datasets
│       - Script auto testing
│
├── logs/                            # Logs for debugging backend
│   └── TODO:
│       - Add logging config
│       - Store API errors
│       - Add conversation log history
│
├── tests/                           # Test folder
│   └── TODO:
│       - Unit test utils
│       - Test API endpoints
│       - Test AI agent outputs
│
├── docs/                            # Documentation folder
│   ├── imgs/                        # TODO: lưu hình kiến trúc hệ thống
│   ├── papers/                      # TODO: tài liệu tham khảo NLP/Agents
│   └── TODO:
│       - System architecture doc
│       - API documentation
│       - Report (for school)
│
└── .gitignore                       # TODO: ignore .env, __pycache__, venv, logs
```