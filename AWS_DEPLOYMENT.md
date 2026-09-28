# PlacePrep — AWS Deployment

This project is prepared for a real AWS production deployment while preserving the existing localhost workflow.

## Architecture

- **AWS Elastic Beanstalk** — runs the existing Flask application with Gunicorn.
- **Amazon RDS for PostgreSQL** — production relational database through `DATABASE_URL`.
- **Amazon S3** — private storage for generated Resume Builder PDFs when `AWS_S3_BUCKET` is configured.
- **Amazon CloudWatch** — Elastic Beanstalk application/platform logs are available through AWS logging; the app also emits structured logs to stdout/stderr.
- **IAM role** — grant the Elastic Beanstalk EC2/service role only the S3 permissions required by the application.

The local environment remains SQLite-based unless `DATABASE_URL` is set.

## Local run

```text
APP_ENV=local
DATABASE_URL=sqlite:///instance/placeprep.db
COOKIE_SECURE=0
```

Windows users can continue to use `run_placeprep.bat`.

## AWS setup

### 1. Create an RDS PostgreSQL database

Create a PostgreSQL database in the same AWS Region as the application. Put it in a private subnet where practical and allow inbound PostgreSQL traffic only from the Elastic Beanstalk application security group.

Set:

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@RDS-ENDPOINT:5432/placeprep
```

The application creates its SQLAlchemy tables on first startup. Existing SQLite data is **not** automatically copied to RDS; export/import it separately if production must contain the existing local records.

### 2. Create a private S3 bucket

Create a private S3 bucket in the same Region. Do not make the bucket public.

Set:

```text
AWS_REGION=ap-south-1
AWS_S3_BUCKET=your-private-placeprep-bucket
AWS_S3_PREFIX=placeprep
```

The Resume Builder uploads generated PDFs to:

```text
placeprep/resumes/user-<id>/resume-<id>.pdf
```

Downloads use short-lived presigned S3 URLs.

### 3. IAM permissions

Attach an IAM policy to the Elastic Beanstalk instance/service role that allows only the required bucket operations, for example:

- `s3:PutObject`
- `s3:GetObject`

Restrict the resources to the PlacePrep bucket/prefix. Do not hard-code AWS access keys in the repository.

### 4. Create an Elastic Beanstalk Python environment

Use the Python platform and upload/connect this project repository. The included `Procfile` starts:

```text
web: gunicorn --workers 2 --threads 4 --timeout 120 app:app
```

Set the environment variables in Elastic Beanstalk Configuration → Environment properties:

```text
APP_ENV=production
SECRET_KEY=<long-random-secret>
DATABASE_URL=postgresql+psycopg://...
AWS_REGION=ap-south-1
AWS_S3_BUCKET=<bucket-name>
AWS_S3_PREFIX=placeprep
AWS_S3_PRESIGNED_SECONDS=900
AWS_CLOUDWATCH_ENABLED=1
COOKIE_SECURE=1
```

### 5. HTTPS and domain

After the environment is healthy, connect a domain through Route 53 or another registrar and configure HTTPS using AWS Certificate Manager/Elastic Load Balancing as appropriate for the chosen Elastic Beanstalk environment.

## Important Coding Arena note

PlacePrep's Coding Arena intentionally uses a Docker isolation boundary. Do not expose the Docker daemon or execute arbitrary student code directly inside the Flask web process. For AWS production, the code runner should be moved to a separate hardened worker/sandbox environment with CPU, memory, process, timeout, filesystem and network restrictions.

## Verification checklist

- [ ] Local `http://127.0.0.1:5000` still starts.
- [ ] AWS Elastic Beanstalk environment is healthy.
- [ ] RDS connection works.
- [ ] Registration/login works against production data.
- [ ] Resume saves to RDS.
- [ ] Resume PDF uploads to private S3.
- [ ] Resume download uses a presigned URL.
- [ ] CloudWatch/Elastic Beanstalk logs are available.
- [ ] Coding Arena execution remains isolated.
- [ ] HTTPS and custom domain are enabled before public use.
