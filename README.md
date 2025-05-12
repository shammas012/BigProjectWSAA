# SMART Service Desk

A web-based ticketing and workflow management system built with Flask, designed to streamline issue tracking and project management.

**Demo**
Application URL: https://shammas012.pythonanywhere.com/

(**using free version of pythonanywhere and sometimes throwing internal server error, if this happens kindly refresh the page**)

**Admin Credentials:**

Username: AndrewB

Password: Admin

**Note:** Please use above credentails with admin rights (Admin role) to access the application. Users with Customer and Agent roles dont have access to User Access Management.

**Table of Contents**

**Features**

**User Authentication:** Secure login system using JWT (JSON Web Tokens).

**User Management:** Create and amend user accounts with saving hashed passwords and options to change password

**Ticket Management:** Create, view and update support tickets.

**Project Management:** Organize tickets under specific projects (created projects using API - no UI).

**Issue Types:** Categorize tickets by predefined issue types (created issue types using API - no UI)..

**Workflows:** Define and manage workflows for ticket processing (created workflows using API - no UI)..

**User Interface:** Responsive UI with AJAX for seamless user experience.

**Logging:** Comprehensive logging system for monitoring and debugging.

**Technology Stack**
**Backend:**

Flask: Web framework.

Flask-JWT-Extended: JWT authentication.

SQLAlchemy: ORM for database interactions.

Flask-Migrate: Handling database migrations.

**Frontend:**

HTML, CSS, JavaScript with AJAX for dynamic content loading.

**Database:**

MySQL

**Hosting:**

PythonAnywhere: Cloud-based hosting platform.

