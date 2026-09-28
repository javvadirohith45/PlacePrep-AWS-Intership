# PlacePrep

PlacePrep is a Flask-based placement-preparation portal with separated Aptitude/Reasoning topic banks, 30-question topic mocks, company assessments, Coding Arena, Top 75 DSA, HR/Technical interviews, Resume Builder, ATS-style checks, analytics, bookmarks and admin content management.

## Windows quick start
1. Install Python 3.11+.
2. Double-click `run_placeprep.bat`.
3. The script creates/uses `venv`, installs dependencies, creates `instance/`, initializes/migrates SQLite and seeds content.
4. Open `http://127.0.0.1:5000`.

## Demo accounts
- Student: `student@placeprep.local` / `Student@123`
- Admin: `admin@placeprep.local` / `Admin@123`

## Important features
- Aptitude and Logical Reasoning are separate.
- Each listed topic receives its own 30-question bank and 20-minute topic mock.
- Questions are retrieved by `topic_id`; unrelated topic questions are never substituted for a shortage.
- Company recruitment links are stored in the database and point to official company career domains.
- Company model-paper records can remain `Coming Soon` until authored content is added.
- Coding execution is isolated behind a Docker runner boundary. PlacePrep does not execute student code in the Flask process. Install/configure Docker to enable real execution.
- Resume PDF generation uses ReportLab.

## Database
Development uses SQLite at `instance/placeprep.db`. Existing SQLite databases are upgraded with lightweight additive migrations at startup; the application does not delete existing data.

## Production / AWS notes
The project is AWS-ready without removing the local development workflow. Production can run the existing Flask application on AWS Elastic Beanstalk with Gunicorn, use Amazon RDS PostgreSQL through `DATABASE_URL`, store generated Resume Builder PDFs in a private Amazon S3 bucket, and use Elastic Beanstalk/CloudWatch logging for operational visibility. Configure a strong `SECRET_KEY`, `COOKIE_SECURE=1`, HTTPS, and an IAM role for S3 instead of hard-coded AWS credentials. See `AWS_DEPLOYMENT.md` for the deployment checklist.

The local version continues to use SQLite at `instance/placeprep.db` when `DATABASE_URL` is not set. Existing SQLite data is not automatically copied into RDS.

The Coding Arena must remain behind a hardened isolated execution boundary; do not execute arbitrary student code inside the Flask web process. Review company recruitment links and assessment patterns periodically because external hiring information can change.

## PlacePrep CodeLab

The Coding Arena has been upgraded as an integrated CodeLab experience. The existing Flask application/database/authentication remain the application boundary; CodeLab adds the coding dashboard, searchable problem library, language tracks, Monaco editor workspace, custom tests, public/hidden test execution, submissions and progress tracking.

### Coding bank
The bundled coding seed contains **260 problems** across C, C++, Java, Python, JavaScript and SQL.

### Real execution
Code execution is intentionally isolated through Docker with network disabled, CPU/memory/pid limits and temporary read-only mounts. Start Docker Desktop before using Run/Submit locally. SQL uses a temporary SQLite database inside the SQL execution container.

### Main CodeLab routes
- `/coding` — CodeLab landing page
- `/coding/problems` — problem library
- `/coding/language/<slug>` — language track
- `/coding/<problem_id>` — coding workspace
- `/coding/dashboard` — authenticated progress dashboard

The execution service is deliberately not a fake result generator: Run uses visible tests, Submit uses hidden tests, and failures are surfaced as wrong answer, compilation error, runtime error or timeout.
