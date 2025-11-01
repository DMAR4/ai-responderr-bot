AI Responder - Deploy on Render (English)

What's included:
- app.py         : Flask app with CORS and OpenAI integration
- rules.json     : Simple rules to match keywords (static or both)
- index.html     : Simple web UI (edit the webhook URL inside)
- requirements.txt
- Procfile
- README.txt (this file)

Quick deploy steps:
1. Create a GitHub repo and push all files.
2. On Render.com, create a new Web Service -> connect your GitHub repo.
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
3. Add an Environment Variable on Render:
   - Name: OPENAI_API_KEY
   - Value: your OpenAI secret key (sk-...)
4. Deploy. Wait for the service URL (e.g., https://your-app-name.onrender.com)
5. Edit index.html: replace https://اسم-تطبيقك.onrender.com/webhook with your service URL + /webhook
6. Open index.html in browser and test.

Notes:
- The app reads PORT from the environment (Render sets it automatically).
- For production, consider restricting CORS origins and securing the endpoint (authentication).
- Monitor Render logs if deployment fails.
