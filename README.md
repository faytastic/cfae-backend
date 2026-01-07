# CFAE Backend  
Live API endpoint: https://cfae.ftlgapps.com/api/contact

Backend service built with Flask.  
Receives contact form submissions, validates data, and returns structured responses.

This service currently runs on the same OCI virtual machine as the frontend, managed by Gunicorn and systemd.  
Over time, this backend will expand to include email notifications, data storage, and automated deployment.

This is the source code for the CFAE backend.  
It is a lightweight Flask API hosted on an OCI compute instance.  
Infrastructure is managed separately, and backend deployments are handled through GitHub Actions.

---

## 🚀 Runtime Overview

This backend runs as a persistent service on the OCI VM.

When the VM boots:

1. systemd automatically starts Gunicorn  
2. Gunicorn loads the Flask application using our factory pattern
3. Nginx (or a future reverse proxy) routes API traffic to the backend  

The service exposes endpoints such as:

    GET /health
    POST /api/contact


This phase focuses on correctness, clarity, and stability before adding external integrations such as email or storage.

---

## 🛠 Service Behavior

- Backend runs continuously under systemd  
- Requests are handled by Gunicorn  
- Input is validated before processing  
- Invalid requests return HTTP 400 responses  
- Logging is currently console-based (will move to structured logs later)  

Backend deployments are automated using GitHub Actions.  
When code is pushed to the main branch, CI verifies the app loads correctly, deploys to the VM, restarts the service, and confirms it is healthy using the `/health` endpoint.



---

## 🔌 API Details

### `/health`

Returns a simple JSON response confirming the backend is running:

    { "status": "ok" }

GitHub Actions uses this endpoint after deployment to verify the service is healthy.


### `/api/contact`

Accepts JSON payload:

    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "message": "Hello from the site!"
    }

Validation rules:

- All fields are required
- Whitespace-only values are rejected

Bad request response (missing field):

    { "error": "All fields are required" }

Successful response:

    {
      "status": "ok",
      "message": "Form received"
    }

---

## 🔄 Deployment (CI/CD)

The backend deploys automatically on every push to the `main` branch.

GitHub Actions runs two workflows:

1. **Backend CI**
   - Installs dependencies
   - Imports the Flask app to confirm it initializes successfully
   - Fails early if configuration or imports are broken

2. **Backend Deploy**
   - Connects securely to the OCI VM using an SSH key stored in GitHub Secrets
   - Syncs the code into `/home/opc/cfae-backend`
   - Restarts the backend service via systemd:

     `sudo systemctl restart cfae-backend`

No manual SSH access is required.  
If a deploy fails, the running version remains untouched.


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
- Automated API tests that run in CI before deployment
- Structured logging  
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

If a deployment causes issues:

1. Revert or roll back the commit in GitHub  
2. Push the revert to `main`  
3. GitHub Actions redeploys the previous working version automatically

If emergency access is needed, the service can still be restarted manually:

    sudo systemctl restart cfae-backend

