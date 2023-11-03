# Refit

## Project Team

- Alison (team lead)
- Sidney (Data Science Manager)
- Vinh (Data Scientist)

- Jared (ICT)
- Christopher (ICT)
- Yael (ICT)

- Mansi Kamani (Cambrian)
- Muqaddas Rahim (Cambrian)
- Nithin Shajan (Cambrian)
- Prashant Tiwari (Cambrian)
- Sumanth Sundar (Cambrian)

## Project Description
Refit is an application to track and manage refridgerant gasses

---

#Project Overview

#### Setup your environment variable

1. Make a copy `.env.example` and rename as `.env`
2. Update the `.env` to have following keys.
   | Key | Description |
   | ------------- | ------------- |
   | MAIL_SERVER | The SMTP server address that will be used to send emails.|
   | MAIL_PORT | The port number that will be used to communicate with the email server. |
   | MAIL_USERNAME | The username that will be used to authenticate with the email server. |
   | MAIL_PASSWORD | The password that will be used to authenticate with the email server. |
   | HASH_SECRET | The secret key that will be used to generate and verify cryptographic hashes for password storage. |
   | ADMIN_EMAIL | The email address of the administrative user for the application. |
   | ADMIN_PASSWORD | The password for the administrative user account. |
   You need to generate an "application-specific password" to use instead of your regular Gmail password.

### Start your project

1. Install your requirements `pip install -r requirements.txt`
2. Run `python3 app.py` or `python app.py`
3. Run migrations `alembic upgrade head`. This should create `app.db` on your root directory
