# 1. ModuleNotFoundError: No module named 'utils.tokenize'
- Put a "__int__.py" in the folder
- If utils is intended to be a package, ensure that it contains an __init__.py file (even if it's empty). This file is necessary to treat a directory as a Python package.

# 2. NotNullViolation: null value in column "user_id" of relation "User" violates not-null constraint
- Because we did not make the user_id in the User table a SERIAL. It is asking us to give a number each time we create a new user which is tedious.
- So we update the code in the uml.py: user_id SERIAL PRIMARY KEY
- And this is how to make them nullable when run uml.py
- CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    email TEXT NULL,
    password TEXT NULL,
    role TEXT NULL,
    added_date TIMESTAMP NULL,
    user_detail TEXT NULL,
    status TEXT NULL
);
