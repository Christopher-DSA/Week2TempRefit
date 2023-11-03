import hashlib
import hmac
import json
import secrets
import string


def generate_hash(message, secret):
    """Generates an HMAC-SHA256 hash of a JSON message using a secret key.

    Args:
        message (dict): A dictionary representing the message to be hashed.
        secret (str): A string representing the secret key to use for hashing.

    Returns:
        str: A hexadecimal string representing the HMAC-SHA256 hash of the message.

    Example:
        >>> message = {'id': 12345, 'name': 'Alice'}
        >>> secret = 'mysecret'
        >>> generate_hash(message, secret)
        'fc40ed98f86e79f16de4e99ccab16aaf727dcedbaade0081f93356fca41e9d3c'
    """
    json_data = json.dumps(message, sort_keys=True)
    # Encode the JSON string as bytes
    message = json_data.encode()

    # Generate the HMAC using SHA-256
    hashed = hmac.new(secret.encode(), message, hashlib.sha256)

    return hashed.hexdigest()


def generate_password():
    """Generates a random 12-character password using ASCII letters and digits.

    Returns:
        str: A randomly generated password consisting of ASCII letters (both upper and
        lower case) and digits.

    Example:
        >>> generate_password()
        'a8GhT9pL6sKw'
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(12))
