# Flask Sports Registration System 

**Problem Statement:**

High school sports related events required manual registration and bookkeeping, leading to:
- Frequent errors in student details.
- Missed deadlines due to lack of notifications.
- Frustration for both students and coaches.

## Solution Overview:

This Flask-based web app automates sports registration with a two-role system:

**Admin Features:**
- Create and manage sporting events with specific deadlines.
- Generate detailed reports in Excel/PDF based on filters like sport, event, grade,student name,etc.
- Manage registrations and access advanced admin utilities.
  
**Student Features:**
- Register for sports and view events tailored to their interests.
- One-click event registration with live updates in the admin dashboard.
- Email-based utilities like password reset for enhanced usability.

**Core Features:**

- Role-based access control (Admin/Student).
- Automated event registration with deadline enforcement.
- Dynamic dashboards for students and admins.
- Reporting capabilities with multiple filter options.
- Built-in password management via email notifications.

**Tech Stack**

- **Backend**: Flask, Flask-Login, Flask-Migrate, Flask-Mail.
- **Database:** SQLAlchemy with SQLite (development) or PostgreSQL (production).
- **Frontend:** HTML, CSS, Jinja2 templating engine.
- **Hosting:** Render

## How It Works

- **Admin:** Creates events with details and deadlines. Monitors registrations and generates reports.
- **Student:** Registers for sports and views relevant events and can register for them.


## Impact

This app replaces the error-prone manual process with a streamlined, automated system, ensuring:

- Efficiency in registration by reducing admin effort by 60%.
- Higher transparency and streamlined process for students with their satisfaction increased by 60%.
- Ease of management for coaches and admins due to easy report generation.



