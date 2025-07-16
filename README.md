	# 🧠 Rock-Paper-Scissors AI Bot

An AI-powered Rock-Paper-Scissors web app that learns your patterns over time using Q-learning and n-gram sequence recognition. Built with:

- ⚙️ **FastAPI** backend
- ⚛️ **React + Vite + TailwindCSS** frontend
- 🐳 **Docker & Docker Compose** for containerized deployment
- 🧠 **Q-Learning + Pattern Recognition** for strategy

---

## 🚀 Features

- Predicts moves using Q-learning based on player history
- Falls back to n-gram pattern recognition for smart guessing
- Fully Dockerized (no local Python/Node setup needed)
- Interactive, sound-enhanced UI with dark mode
- API ready for integration or extension

---

## ⚙️ Setup Instructions

### 🐳 Using Docker (Recommended)

Make sure Docker & Docker Compose are installed.

```bash
# Clone the repo
git clone https://github.com/hemanthsukumar/RPSBOT.git
cd RPSBOT

# Train the Q-learning bot (optional, pre-trained model is included)
cd backend
python app/train.py
cd ..

# Build and run the entire stack
docker-compose up --build

	•	Backend: http://localhost:8000
	•	Frontend: http://localhost:5173

⸻

🧪 API Usage

POST /move

Predict the bot’s next move based on your previous choices.

Request Body

{
  "history": ["rock", "paper", "rock"]
}

Response

{
  "bot_move": "scissors",
  "confidence": 0.83,
  "strategy": "ngram"
}

GET /ping

Check if the backend is alive.

{ "message": "Bot is alive!" }


⸻

⚒️ Dev Mode (no Docker)

Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Frontend

cd frontend
npm install
npm run dev


⸻

🧠 How It Works
	•	Q-Learning maps recent player moves to optimal bot actions.
	•	N-gram Matching detects frequent patterns (like “rock, paper, rock”) and counters them.
	•	Bot combines both approaches for smarter decisions.

⸻

🛡️ Notes
	•	Q-table is stored at backend/app/q_table.pkl
	•	BOT_TEMPERATURE in .env controls randomness (lower = more confident)
	•	Update the Q-table by re-running train.py
	•	Avoid exposing unrestricted CORS origins (*) in production

⸻

📦 Credits & License

Created by Hemanth Sukumar Vangala.
Open-sourced under MIT License.

---
