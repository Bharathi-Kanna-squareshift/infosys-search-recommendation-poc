# Infosys Search Recommendation POC

Backend: Python/Flask
Frontend: React (`infosys-demo-ui`)

## Prerequisites

*   Git
*   Python 3.8+ & pip
*   Node.js 16+ & npm

## Setup & Run

**1. Clone Repo**

```bash
git clone https://github.com/Bharathi-Kanna-squareshift/infosys-search-recommendation-poc.git
cd infosys-search-recommendation-poc
```

**2. Setup Backend**

```bash
# Create & activate virtualenv (macOS/Linux example)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment (create backend/.env if needed)
# cp backend/.env.example backend/.env # If example exists
# Set FLASK_APP=run:app or FLASK_APP=app in backend/.env (verify!)
```

**3. Setup Frontend**

```bash
# Navigate & install dependencies
cd infosys-demo-ui
npm install

# Configure environment (create .env.local if needed)
# cp .env.example .env.local # If example exists
# Set REACT_APP_API_BASE_URL=http://localhost:5000 (or backend port) in .env.local

# Navigate back to root (optional)
cd ..
```

**4. Run Application**

*   **Terminal 1: Run Backend**
    *   Ensure `.venv` is active (`source .venv/bin/activate`)
    *   Run from project root: `flask run` (or `python backend/run.py` - verify command)
    *   *(Backend typically runs on http://localhost:5000)*
*   **Terminal 2: Run Frontend**
    *   Navigate to frontend: `cd infosys-demo-ui`
    *   Run: `npm start`
    *   *(Frontend typically runs on http://localhost:3000)*

Access the application via the frontend URL (e.g., `http://localhost:3000`).
