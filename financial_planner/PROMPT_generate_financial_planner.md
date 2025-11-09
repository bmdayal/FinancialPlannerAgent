# Single-Prompt Specification: Generate Financial Planner Web App

Purpose
-------
This is a single, self-contained developer prompt you can paste into an AI assistant to generate a complete Flask + Plotly financial planner web application from scratch. The generated project should include the server, templates, static JS/CSS, dependencies, environment handling, and a chatbot integrated with OpenAI.

Requirements / Acceptance Criteria
---------------------------------
- Language: Python 3.10+ (or latest compatible)
- Web framework: Flask
- Charts: Plotly (rendered client-side via plotly.js using JSON payloads from server)
- Virtual environment friendly, with a `requirements.txt`
- Environment variables loaded from a `.env` file (python-dotenv)
- The OpenAI API key must be read from environment variable `OPENAI_API_KEY`, never hard-coded
- A minimal, clean UI using Bootstrap
- Chatbot using OpenAI Chat Completions API and server-side wrapper with error handling
- Clear README with setup and run instructions
- All produced source files placed under a single folder `financial_planner/`

Project Structure to generate
-----------------------------
financial_planner/
- app.py
- requirements.txt
- .env (example with placeholder)
- README.md
- templates/
  - base.html
  - index.html
  - input.html
- static/
  - chat.js
- (optional) run_local.ps1

Detailed Functional Requirements
-------------------------------
1. app.py
   - Provide endpoints:
     - `GET /` -> index page
     - `GET /input` -> form input page
     - `POST /calculate` -> accept JSON data, run calculations (retirement projection, education costs, monthly savings), return JSON with Plotly figure JSON for each chart and `analysis` block summarizing risks and recommendations
     - `POST /chat` -> accept JSON with `message` and the user's `financialData` object, maintain session chat-history, send system+history+user messages to OpenAI, return assistant response
   - Add helper functions:
     - `generate_plots(user_profile)` returns dict with `retirement`, `education`, `monthly`, etc. as Plotly JSON
     - `analyze_financial_health(user_profile, plots)` returns `summary`, `risks`, `recommendations` keys
   - Load `.env` using python-dotenv, read `OPENAI_API_KEY`. Print a warning if not set.
   - Wrap OpenAI calls in a helper with robust error handling and logging
   - Use `app.secret_key` for session and keep chat history in `session`

2. templates/base.html
   - Include Bootstrap and Plotly.js
   - Provide a dark theme CSS block
   - Include chat UI elements (toggle button, chatbox container) that will be populated by `static/chat.js`

3. templates/index.html
   - Simple welcome page with button to navigate to `/input`

4. templates/input.html
   - Form fields: age, current_savings, annual_income, retirement_age, num_children
   - When `num_children` changes, dynamically add child blocks (age, education goal)
   - On form submit, send JSON to `/calculate`, then render Plotly charts with `Plotly.newPlot(div, response.plot.data, response.plot.layout)` pattern (server returns `fig.to_json()` parsed into `{data, layout}` on client), and show analysis summary above charts
   - After successful calculation, show chat toggle button

5. static/chat.js
   - Provide a small chat UI client: opening/closing, message list, input box, send button
   - When sending, POST JSON to `/chat` with keys `message` and `financialData` (the same object used to calculate plots)
   - Append user and assistant messages to message list
   - Minimal retry/error messages on network failure

6. requirements.txt
   - Minimal pinned libs: flask, plotly, numpy, python-dotenv, openai

7. README.md
   - Full setup and run instructions (Windows PowerShell commands, venv, pip install, set env var, run flask)
   - How to use the UI and chat
   - Troubleshooting tips

Security & Best Practices
-------------------------
- Do not commit `.env` to git
- Use descriptive error messages when helpful but do not leak sensitive info
- Use `max_tokens` and rate-limiting considerations for API calls
- Keep chat history limited to last N messages in session when sending context (e.g., last 5)

Testing & Verification
----------------------
- Add a quick manual test procedure in README that covers:
  1. Start server
  2. Navigate to `/input`
  3. Enter realistic sample data (age 35, savings $100k, income $85k, retirement 65, 2 children aged 5 and 2)
  4. Click Calculate and confirm charts appear and analysis is provided
  5. Click chat, ask "Will I run out of money in retirement?" and confirm assistant replies using numbers from the analysis

Output expectations for the generator
-------------------------------------
- Create all files described above
- Ensure `app.py` runs without syntax errors and endpoints return JSON shapes matching what's expected by the front-end
- Provide a `requirements.txt` that includes the packages necessary for the code

If you want the generator to produce code in small increments, add: "Output files only; do not run code; provide any necessary setup commands at the end." Otherwise generate the full project files and example `.env` placeholder.

---

Notes for reuse: paste the entire contents of this prompt into an LLM (or a code generation assistant) and instruct it to `create files at path financial_planner/*` and produce the files exactly as requested. If the assistant supports multiple steps, ask it to return each file's content in code fences labelled with the filepath.

