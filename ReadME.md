# Thiran | திறான் - Connecting Skills, Building Futures

[![Build Status](https://img.shields.io/badge/build-passing-green)](https://github.com/) [![Code Quality](https://img.shields.io/badge/quality-B-yellow)](https://github.com/) [![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/)

**Thiran is a web platform built with Flask and MySQL, designed to bridge the gap between skilled daily wage workers and customers. It provides a straightforward, on-demand service for finding and hiring local talent.**

---

## 🎯 The Problem

India's informal sector employs over 90% of the workforce, yet it remains largely unorganized. Skilled workers often face uncertain daily earnings, while customers struggle to find reliable and verified help quickly. Thiran aims to digitize this process, bringing efficiency and opportunity to this vital part of our economy.

## ✨ Our Solution: Thiran

Thiran creates a simple and effective marketplace connecting two key groups: "Users" (employers) who need a job done, and "Workers" who have the skills to do it. Our platform allows users to post jobs and enables workers to find and accept work that matches their skillset.

### Key Implemented Features

* **Dual User Roles:** Separate registration and login portals for both Workers and Users (Employers).
* **Skill-Based Registration:** Workers can select multiple skills during registration (e.g., Electrician, Plumber, Tailor).
* **Job Posting:** Registered users can post new jobs, specifying the title, description, address, and the specific skill required.
* **Worker Dashboard:** Workers have a personalized dashboard that shows a list of all available "Open" jobs that match their registered skills.
* **Job Acceptance Workflow:** Workers can accept a job directly from their dashboard, which updates the job's status to "Assigned" and links the worker to the job.

## 🛠️ Technology Stack & Architecture

The application is built using a classic web stack, chosen for its robustness and rapid development capabilities.

* **Backend:** Python, Flask  
* **Database:** MySQL (interfaced using Flask-MySQLdb)  
* **Frontend:** HTML, CSS (using Jinja2 templating)  
* **Session Management:** Utilizes Flask's secure session handling for user and worker logins.

### Database Schema

The application's functionality is supported by a relational database schema consisting of five main tables:

1. `users`: Stores employer information (username, password, phone).
2. `workers`: Stores worker information (name, password).
3. `skills`: A static table containing all available skills (e.g., Plumber, Electrician).
4. `worker_skills`: A many-to-many link table connecting workers to their respective skills.
5. `jobs`: Contains all job details, including title, description, status, and the IDs linking to the employer and assigned worker.

## ⚙️ Getting Started (Local Setup)

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.9+
* MySQL Server
* Git

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/thiran.git
    cd thiran
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install Flask Flask-MySQLdb mysql-connector-python
    ```

4. **Set up the database:**
    * Ensure your MySQL server is running.
    * Update the MySQL credentials in `app.py` to match your local setup:
        ```python
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'your_password'  # Change this
        ```

5. **Run the application:**
    ```sh
    python app.py
    ```
    The application will automatically create the `thiran_db` database and necessary tables on the first run. It will be available at `http://127.0.0.1:5000`.

## 📈 Future Scope & Areas for Improvement

This project provides a solid foundation. To enhance it further, we plan to:

* **🔐 Implement Password Security:** Integrate password hashing (e.g., using Werkzeug security helpers) to avoid storing passwords in plain text.
* **🤖 Develop AI-Powered Matching:** Move beyond simple skill filtering to an intelligent algorithm that ranks the best workers for a job based on location, ratings, and job history.
* **⭐️ Introduce a Two-Way Rating System:** Allow both users and workers to rate each other to build trust and accountability.
* **💬 Add In-App Communication:** A messaging feature for users and workers to communicate directly.
* **✅ Create a Skill Verification Process:** A system to verify worker skills beyond self-declaration.

## 👥 Meet the Team

| Name            | Role           | GitHub Profile                                  |
|-----------------|----------------|--------------------------------------------------|
| Harshil Garg  | Back-end       | [https://github.com/H4R5H1L-27](https://github.com/your-username) |
| Kartik Mangla   | Front-end      | [https://github.com/kavish12345678](https://github.com/kavish12345678) |
