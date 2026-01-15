# Clinic Follow-up Tracker (Lite)

A simple Django application for tracking clinic follow-ups.
Users belong to a clinic and can manage follow-ups for their own clinic only.
Patients can view follow-up instructions using a public link.


## Requirements

- Python 3.10+
- Django 5.x
- SQLite (default)


## Setup Instructions

1. Clone the repository or unzip the project.

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```
   python manage.py migrate
   ```

5. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```
   python manage.py runserver
   ```


## Initial Data Setup

After logging into the Django admin panel at http://127.0.0.1:8000/admin/:

1. Create a Clinic.
2. Create a User (if not already created).
3. Create a UserProfile linking the user to the clinic.


## Using the Application

- Login at: http://127.0.0.1:8000/accounts/login/
- After login, users are redirected to the dashboard.
- Users can create, edit, and mark follow-ups as done.
- Each follow-up has a public link accessible without login.


## CSV Import

A sample CSV file is included at `sample.csv` in the project root.

Run the import command:

```
python manage.py import_followups --csv sample.csv --username <your_username>
```

Replace `<your_username>` with an existing username that has a UserProfile.

Invalid rows are skipped and a summary is printed.


## Running Tests

Run all tests using:

```
python manage.py test
```


## Project Structure

```
clinic_tracker/
├── manage.py
├── README.md
├── requirements.txt
├── sample.csv
├── clinic_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── followups/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── import_followups.py
└── templates/
    ├── base.html
    ├── login.html
    └── followups/
        ├── dashboard.html
        ├── followup_form.html
        └── public_view.html
```


## Design Notes

- Access control is enforced at the view level using clinic-based filtering.
- Public links use secure, non-guessable tokens.
- Templates are intentionally minimal and logic-free.
- Tests focus on access control, token generation, and public view logging.
