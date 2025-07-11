# SaleSync - Django & Tailwind CSS Point-of-Sale System

SaleSync is a modern, responsive web application for managing product sales. Built with Django on the backend and styled with Tailwind CSS, it provides a clean and efficient interface for handling products, sales, and reporting.

<!-- Optional: Add a GIF or screenshot of your app here -->
<!-- ![SaleSync Demo](./demo.gif) -->


## Features

-   **User Authentication**: Secure login/logout system for staff, with a protected admin area.
-   **Product Management (CRUD)**: Easily add, view, edit, and delete products with image uploads.
-   **Dynamic Sales Interface**: A JavaScript-powered point-of-sale page to add items to a cart in real-time.
-   **Sales History & Filtering**: View a list of all past transactions with a simple and effective date filter.
-   **Printable Receipts & Reports**: Generate and print individual sales receipts and summary sales reports with a date range filter.
-   **Responsive UI**: A mobile-first design with a hamburger menu that works seamlessly on desktops, tablets, and phones.
-   **Global User Feedback**: Color-coded, dismissible messages for actions like "Product Saved" or "Error".

## Tech Stack

-   **Backend**: Django
-   **Frontend**: Tailwind CSS
-   **JavaScript**: Vanilla JS for dynamic UI elements
-   **Integration**: `django-tailwind`
-   **Database**: SQLite 3 (default)

---

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

-   Python 3.8+
-   Pip & a virtual environment tool (`venv`)
-   Node.js and npm

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mhafiz71/sales_sync.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment to install Python dependencies::**
    ```bash
    # Install pipenv
    pip install pipenv

    # Install project dependencies
    pipenv install

    # You may need to activate environment with
    pipenv shell
 
    ```

3.  **Install and build frontend dependencies:**
    This command initializes Tailwind CSS and installs its node modules.
    ```bash
    python manage.py tailwind install
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to log in:**
    Follow the prompts to create your admin account.
    ```bash
    python manage.py createsuperuser
    ```

---

## Running the Application

This project requires **two concurrent terminal sessions** to run properly.

**1. Start the Tailwind CSS compiler:**
This terminal will watch for changes in your template files (`.html`) and recompile your CSS automatically.

```bash
python manage.py tailwind start
```

**2. Start the Django development server:**
In a **new terminal** (while the first one is still running), start the Django server.

```bash
python manage.py runserver
```

You can now access the application at **http://127.0.0.1:8000/**. Log in with the superuser credentials you created.

---

## Project Structure

```
sales_sync/
├── core/                  # Main Django app for all business logic
│   ├── migrations/
│   ├── templates/core/    # HTML templates for the app
│   ├── forms.py           # Product and other forms
│   ├── models.py          # Database models (Product, Sale, etc.)
│   ├── views.py           # Request/response logic
│   └── ...
├── sales_project/             # Django project settings
│   ├── settings.py
│   └── urls.py
├── theme/                 # App for Tailwind CSS assets
│   ├── static_src/        # Source CSS files
│   └── templates/base.html # Main layout template
├── media/                 # (Generated) Stores uploaded product images
├── manage.py              # Django's command-line utility
└── README.md              # This documentation file
```

---
