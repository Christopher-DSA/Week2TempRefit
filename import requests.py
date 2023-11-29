import requests

# Replace 'YOUR_JWT_TOKEN' and the URL with the actual token and reset password link
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTA1MTM2OSwianRpIjoiNDMwMjA4NjYtYTEzMy00YjA3LWFiZjMtYTJiZDYzYmNlYWIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmdvdF9wYXNzd29yZF90ZXN0QGVtYWlsLmNvbSIsIm5iZiI6MTcwMTA1MTM2OSwiZXhwIjoxNzAxMDUyMjY5fQ.vXTQTBRALnO6GW2bpo3dhqv1X3k_WJnYJSMu11j5V6k'
reset_password_url = 'http://172.16.224.205:5000/reset_password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTA1MTM2OSwianRpIjoiNDMwMjA4NjYtYTEzMy00YjA3LWFiZjMtYTJiZDYzYmNlYWIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmdvdF9wYXNzd29yZF90ZXN0QGVtYWlsLmNvbSIsIm5iZiI6MTcwMTA1MTM2OSwiZXhwIjoxNzAxMDUyMjY5fQ.vXTQTBRALnO6GW2bpo3dhqv1X3k_WJnYJSMu11j5V6k'

# Set up the headers with the Authorization header and JWT token
headers = {'Authorization': f'Bearer {jwt_token}'}
timeout = 60
# Make the GET request with the headers
response = requests.get(reset_password_url, headers=headers,timeout=timeout)

# Print the response
print(response.text)

