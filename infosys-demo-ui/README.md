# Search App Project

This project consists of a Python Flask backend and a React frontend (`infosys-demo-ui`). This guide explains how to set up and run both components locally.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Git:** To clone the repository.
*   **Python:** Version 3.8 or higher recommended. (Check with `python --version` or `python3 --version`)
*   **pip:** Python package installer (usually comes with Python).
*   **Node.js:** Version 16 or higher recommended. (Check with `node --version`)
*   **npm:** Node package manager (usually comes with Node.js). (Check with `npm --version`)

## Setup Instructions

Follow these steps to get the project running:

**1. Clone the Repository**

   Open your terminal or command prompt and run:

   ```bash
   git clone <your_repository_url>
   cd search-app
Use code with caution.
Markdown
Replace <your_repository_url> with the actual URL of your Git repository.
2. Set Up the Backend (Python/Flask)
Navigate to Project Root (if not already there):
Make sure your terminal is in the search-app root directory.
Create and Activate a Python Virtual Environment:
It's highly recommended to use a virtual environment to manage Python dependencies. The .venv directory is already ignored by the suggested .gitignore.
# Create the virtual environment (use python3 if python is linked to Python 2)
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (Git Bash):
# source .venv/Scripts/activate
# On Windows (Command Prompt):
# .venv\Scripts\activate.bat
Use code with caution.
Bash
You should see (.venv) prefixing your terminal prompt after activation.
Install Backend Dependencies:
Install the required Python packages listed in backend/requirements.txt.
pip install -r backend/requirements.txt
Use code with caution.
Bash
Configure Backend Environment Variables:
The backend might require environment variables (e.g., API keys, database URLs, Flask settings). There is a .env file listed in the backend directory structure, which is likely ignored by Git.
You need to create your own backend/.env file. If a backend/.env.example file exists, copy it:
# If backend/.env.example exists:
cp backend/.env.example backend/.env
# Otherwise, create backend/.env manually
Use code with caution.
Bash
Edit backend/.env and fill in the necessary values. Common variables might include:
# Example backend/.env content
FLASK_APP=app # Or the main entry point file like run.py
FLASK_ENV=development # Set to 'production' for deployment
# Add other variables like SECRET_KEY, DATABASE_URL, etc. if needed
# SECRET_KEY=your_very_secret_key_here
Use code with caution.
Dotenv
Make sure FLASK_APP points to the correct Flask application instance (e.g., app if your main file is app.py and contains app = Flask(__name__), or run:app if it's run.py). Looking at your structure, FLASK_APP=app (referring to the app directory/package) or FLASK_APP=run:app (if run.py creates the app instance named app) are likely candidates. Adjust based on your actual run.py or app/__init__.py.
3. Set Up the Frontend (React/Node.js)
Navigate to the Frontend Directory:
cd infosys-demo-ui
Use code with caution.
Bash
Install Frontend Dependencies:
Install the required Node.js packages listed in package.json.
npm install
Use code with caution.
Bash
Configure Frontend Environment Variables (if necessary):
Similar to the backend, the frontend might need environment variables (e.g., the backend API endpoint URL). React apps often use .env files (like .env.local). Check if an .env.example exists in the infosys-demo-ui directory.
# If infosys-demo-ui/.env.example exists:
cp .env.example .env.local
# Otherwise, create .env.local manually if needed
Use code with caution.
Bash
Edit .env.local and add necessary variables. For React (using Create React App), variables usually need to start with REACT_APP_.
# Example infosys-demo-ui/.env.local content
REACT_APP_API_BASE_URL=http://localhost:5000 # Or whatever port the backend runs on
Use code with caution.
Dotenv
Navigate Back to Project Root (optional but recommended for next step):
cd ..
Use code with caution.
Bash
Running the Application
You need to run both the backend and frontend servers simultaneously. Open two separate terminal windows/tabs for this.
Terminal 1: Run the Backend Server
Make sure you are in the search-app root directory.
Ensure the Python virtual environment is activated (source .venv/bin/activate).
Run the Flask development server:
# Ensure FLASK_APP is set correctly in backend/.env
# Then run from the root directory:
flask run
# OR, if your entry point is run.py:
# python backend/run.py
# OR, navigate into the backend first:
# cd backend
# flask run
Use code with caution.
Bash
The backend server should start, typically on http://127.0.0.1:5000/. Check the terminal output for the exact address.
Terminal 2: Run the Frontend Server
Navigate to the frontend directory:
cd infosys-demo-ui
Use code with caution.
Bash
Run the React development server:
npm start
Use code with caution.
Bash
The frontend development server should start and automatically open in your web browser, typically at http://localhost:3000/.
