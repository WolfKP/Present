# Present

Present is a web application built with Python, HTML, and CSS, designed for music teachers to efficiently track and communicate their studio's attendance. It also offers an easy-to-use interface for handling basic student information and calculating related summary statistics.

## Features and Quirks

- The application provides secure user signup and login.
- Teachers can add students to their studio with details such as name, age, sex, and other relevant data to receive summary statistics like the studio's average age and sex makeup.
- Attendance records can be sent to the designated recipients via email, with teachers able to specify the attendance date in addition to each student's status (either present, absent with 24-hour notice, or no-show). The emails are formatted neatly with HTML and CSS, and details such as the teacher's name (user name) and email are automatically populated.
- Teachers can search past attendance records by date.
- Teachers can update their account settings including user name, email and password, in addition to managing their studio and attendance history data with one click.

## Local Installation

1. Clone the repository:

    ```
    git clone https://github.com/yourusername/Present.git
    ```

2. Inside the repository, set up a virtual environment and activate it:
    
    ```
    cd Present
    python -m venv env
    source env/bin/activate
    ```

3. Install the required libraries:

    ```
    pip install -r requirements.txt
    ```

4. Create the instance directory:

    ```
    mkdir instance
    ```

5. Inside the instance directory, specify your configurations in config.py:

    ```
    cd instance
    touch config.py
    ```

  - The contents of config.py should be something like:

    ```
    SECRET_KEY = "your_secret_key" # Replace

    MAIL_SERVER = "smtp.gmail.com" # Replace
    MAIL_PORT = 587 # Typically 587 for TLS
    MAIL_USE_TLS = True
    MAIL_USERNAME = "your_email@gmail.com"  # Replace
    MAIL_PASSWORD = "your_app_specific_or_email_service_password"  # Replace

    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"  # Adjust as needed
    ```

## Running Locally

- To run the application after installation, navigate to the cloned repository in your terminal, activate the virtual environment, do `flask run`, and then go to http://127.0.0.1:5000/ in your browser.

## Deployment

  - For deploying the application, please refer to Flask's official [deployment documentation](https://flask.palletsprojects.com/en/latest/deploying/).