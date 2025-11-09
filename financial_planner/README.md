# Financial Planner Web Application

This Flask-based Financial Planner helps users estimate retirement and education savings needs and visualize projections with Plotly. It also includes a small OpenAI-backed chatbot for follow-up questions.

## Features
- Input form for: current age, current savings, annual income, target retirement age, and dynamic child entries (age + education goal).
- Four interactive Plotly charts:
  - Retirement savings projection (line chart)
  - Projected education costs by child (bar chart)
  - Monthly savings requirements (bar chart)
  - Combined monthly savings distribution (sunburst)
- Financial health analysis summary (risk level, recommendations)
- OpenAI-powered chatbot that uses the current analysis and inputs as context to answer further questions

## File structure

financial_planner/
- app.py                # Flask application and API endpoints
- requirements.txt      # Python dependencies
- .env                  # Environment variables (OPENAI_API_KEY)
- templates/
  - base.html
  - index.html
  - input.html
- static/
  - chat.js
- README.md
- financial_planner_app.md  # design notes / plan


## Setup (Windows / PowerShell)

Open PowerShell and run the following (copy-paste):

```powershell
cd C:\Repos\AgenticAIDemo\financial_planner
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # or: .\.venv\Scripts\activate
pip install -r requirements.txt
```

If PowerShell blocks script execution, run (one-time, CurrentUser scope):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Environment variables

Create a `.env` file in the `financial_planner` directory with the following content:

```
OPENAI_API_KEY=sk-...
```

Do not commit `.env` to version control. Keep keys secret.

## Run the app

From the project folder and with the virtualenv activated:

```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "1"
flask run
```

Open http://localhost:5000 in your browser.

## Using the app
1. Click "Start Planning" on the home page.
2. Fill your financial info and the number of children.
3. For each child, provide age and education goal.
4. Click Calculate to view analysis and charts.
5. After submission, a chat icon appears. Click it to ask follow-up questions. The chatbot will use your submitted data and the generated analysis as context.

## How the chatbot uses context
The chat endpoint receives your message and the most recent financial data. The app builds a compact context string with these items:
- personal info (age, income, savings)
- retirement projection and years covered
- monthly savings requirements
- per-child education costs and monthly needs

This ensures the assistant's replies are tailored to your numbers.

## Troubleshooting
- If charts don't render in Jupyter / notebook: ensure `nbformat>=4.2.0` is installed (not required for the web app).
- If chat returns errors:
  - Confirm `OPENAI_API_KEY` in `.env` is valid
  - Check console logs in the Flask terminal for error messages
- If PowerShell refuses to activate the venv, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in an elevated PowerShell session.

## Development notes
- The app is intentionally minimal and uses Plotly's JSON output to render charts client-side.
- The chatbot uses the `gpt-3.5-turbo` model via OpenAI's Chat Completions API in a helper wrapper with improved error handling.

## Security note
- Never commit your `.env` or API keys to public repositories.

## Next steps / Enhancements
- Add persistent storage (SQLite) to save scenarios
- Improve unit tests and add CI
- Add user authentication
- Add downloadable PDF reports

---

If you want, I can add a small `run_local.ps1` helper script that prepares the virtualenv and starts the server with one command.