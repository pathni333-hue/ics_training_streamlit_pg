# ICS Training Streamlit App (PostgreSQL Version)

This app teaches key OT/ICS cybersecurity concepts using six interactive labs.  
Now upgraded with PostgreSQL authentication, persistence, and PDF reports.

---

## 🔧 Setup (Local or Server)
1. Unzip and open this project.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set PostgreSQL environment variables (adjust values):
   ```bash
   export PGHOST=your-host
   export PGPORT=5432
   export PGDATABASE=your-db
   export PGUSER=your-user
   export PGPASSWORD=your-password
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deploy to Streamlit Cloud
1. Push this repo to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Add the same environment variables in “Advanced Settings → Secrets”.
4. Deploy.

Use Neon.tech or Railway.app for free managed PostgreSQL.
