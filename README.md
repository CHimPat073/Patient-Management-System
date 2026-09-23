# Patient Management API

A beginner FastAPI project for managing patient records with MySQL, SQLAlchemy, and Pydantic.

## What Has Been Built

- FastAPI application with interactive Swagger documentation.
- Pydantic validation for patient input.
- Computed response fields:
	- `bmi`
	- `verdict`
	- `treatment`
- SQLAlchemy model for the MySQL `patient_db` table.
- MySQL connection loaded securely from a local `.env` file.
- Database session dependency with automatic session cleanup.
- JSON-to-MySQL migration script in `seed_database.py`.
- CRUD endpoints:
	- `POST /create` creates a patient in MySQL.
	- `GET /veiw` returns all patients from MySQL.
	- `GET /veiw/{patient_id}` returns one patient from MySQL.
	- `PUT /edit/{patient_id}` updates selected patient fields in MySQL.
	- `DELETE /delete/{patient_id}` deletes a patient from MySQL.

## Project Structure

```text
main.py          FastAPI routes and Pydantic models
database.py      SQLAlchemy engine and database sessions
models.py        SQLAlchemy database table models
seed_database.py Imports patients.json into MySQL
req.txt          Python dependencies
pyproject.toml   Project metadata and uv build configuration
uv.lock          Locked dependency versions
.env             Local database URL; do not commit this file
```

## Requirements

- Python 3.11 or newer
- MySQL Server running locally on port `3306`
- A MySQL database named `patients_db`

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
uv venv
uv pip install --python ".\.venv\Scripts\python.exe" -r req.txt
```

Create a local `.env` file:

```env
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/patients_db
```

Replace `YOUR_PASSWORD` with your local MySQL password.

To import the original JSON records into MySQL:

```powershell
& ".\.venv\Scripts\python.exe" seed_database.py
```

Start the API:

```powershell
& ".\.venv\Scripts\python.exe" -m uvicorn main:app --reload
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Computed Fields

The database stores the source values such as height, weight, and diagnosis. It does not store `bmi`, `verdict`, or `treatment`. These values are calculated by the Pydantic model when a patient is returned by the API.

## Sorting Patients

The `/sort` endpoint reads patient records from MySQL and sorts them by `age` or `last_visit` in ascending or descending order.

## GitHub Safety

The following local content is excluded by `.gitignore`:

- `.env`
- `.venv/`
- `patients.json`
- `pydantic/`
- Python cache files

Never commit database passwords or real patient data.
