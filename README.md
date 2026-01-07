# CFAE Backend  
Live API endpoint: https://cfae.ftlgapps.com/api/contact

Backend service built with Flask.  
Receives contact form submissions, validates data, and returns structured responses.

This service currently runs on the same OCI virtual machine as the frontend, managed by Gunicorn and systemd.  
Over time, this backend will expand to include email notifications, data storage, and automated deployment.

This is the source code for the CFAE backend.  
It is a lightweight Flask API hosted on an OCI compute instance.  
Infrastructure is managed separately, and backend deployments are currently manual while the service is evolving.

---

## 🚀 Runtime Overview

This backend runs as a persistent service on the OCI VM.

When the VM boots:

1. systemd automatically starts Gunicorn  
2. Gunicorn loads the Flask application (app.py)  
3. Nginx (or a future reverse proxy) routes API traffic to the backend  

The service exposes endpoints such as:

    GET /
    POST /api/contact

This phase focuses on correctness, clarity, and stability before adding external integrations such as email or storage.

---

## 🛠 Service Behavior

- Backend runs continuously under systemd  
- Requests are handled by Gunicorn  
- Input is validated before processing  
- Invalid requests return HTTP 400 responses  
- Logging is currently console-based (will move to structured logs later)  

Manual SSH may be used temporarily for updates or troubleshooting.  
Backend deployments are currently manual while the service evolves. CI/CD automation is planned.


---

## 🔌 API Details

### /

Basic health endpoint confirming the backend is running.

### /api/contact

Accepts JSON payload:

    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "message": "Hello from the site!"
    }

Validation rules:

- All fields are required  
- Whitespace-only values are rejected  

Bad request response:

    { "error": "All fields are required" }

Successful response:

    {
      "status": "ok",
      "message": "Form received"
    }

---

## 🔄 Deployment (current workflow)

Until CI/CD is added, backend updates are deployed manually:

    cd ~/cfae-backend
    git pull
    sudo systemctl restart cfae-backend

The service restart ensures the latest code is loaded into Gunicorn.  
Once backend features stabilize, deployment will move to a controlled CI/CD pipeline similar to the frontend.

---

## 🧾 Logging

Currently:

- Requests log to console  
- systemd stores service logs  

View logs:

    sudo journalctl -u cfae-backend -f

Structured log files will be added as the system grows.

---

## 🔐 Security Notes

- No secrets are stored in code  
- API accepts only JSON payloads  
- HTTPS is enforced at the infrastructure level  
- .gitignore prevents sensitive or unnecessary files from being committed  
- The VM authenticates to GitHub securely using SSH keys  

Future enhancements include env-based configuration and secret management.

---

## 🚧 Roadmap

Planned backend enhancements:

- Email notifications on form submission  
- Persistent storage (database or object storage)  
- Environment variable configuration  
- Structured logging  
- CI/CD pipeline for backend deployments  
- Monitoring and error tracking  
- Authentication for administrative endpoints  

---

## 🛠 Technologies Used

- Python / Flask  
- Gunicorn  
- systemd  
- Oracle Cloud Infrastructure (Compute)  
- GitHub version control  

---

## 📂 Key Paths on the VM

- Backend repo: /home/opc/cfae-backend  
- Backend service runs via Gunicorn under systemd  
- Logs available via journalctl  

---

## ♻️ Rollback

If a backend change causes issues:

1. Revert to a previous commit in GitHub  
2. Pull the previous version on the VM  
3. Restart the backend service  

    git checkout <previous_commit>
    sudo systemctl restart cfae-backend

Rollback stabilizes production while fixes are prepared.
