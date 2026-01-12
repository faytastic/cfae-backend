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
- Deployments are health-gated via the `/health` endpoint

Backend deployments are automated using GitHub Actions.  
When code is pushed to the main branch, CI verifies the app loads correctly, deploys to the VM, restarts the service, and confirms it is healthy using the `/health` endpoint.



---

## 🔌 API Details

### `/health`

Returns a simple JSON response confirming the backend is running:

    { "status": "ok" }

GitHub Actions uses this endpoint after deployment to verify the service is healthy.  
The endpoint is implemented in the backend route layer and exists solely for deployment health checks.



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
If a deploy fails its health check, the backend automatically rolls back to the last known good version and continues running without manual intervention.


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

- No secrets are stored in code or committed to Git  
- Secrets are injected at runtime via GitHub Actions and systemd  
- Production requires a valid `SECRET_KEY` and fails fast if missing  
- HTTPS is enforced at the infrastructure level


---

## 🚧 Roadmap

Planned backend enhancements:

- Email notifications on form submission  
- Persistent storage (database or object storage)  
- Automated API tests (request/response validation) that run in CI before deployment
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

## ♻️ Automatic Rollback

Backend deployments are protected by an automatic rollback mechanism.

During each deploy:

1. The currently running commit hash is recorded as the last known good version
2. The new code is deployed and the service is restarted
3. GitHub Actions calls the `/health` endpoint to verify the service

If the health check fails:
- The backend automatically checks out the previous known good commit
- The service is restarted again
- The deployment is marked as failed in GitHub Actions
- The backend continues running on the last healthy version

The currently trusted version is tracked on the VM in:

    /home/opc/cfae-backend/.last_known_good_commit

This ensures failed deployments do not take the service offline.
