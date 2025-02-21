import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMTIyNjcyLCJpYXQiOjE3NDAxMjA4NzIsImp0aSI6ImQ1Y2FiYTUxMjJkZTRhOWFhZDZhODA1MDdkZGRmNTAxIiwidXNlcl9pZCI6MX0.TN48IShRelslJPFV2wLfjc6A62XBwIxpQGTZqP_GZRc"
decoded = jwt.decode(token, options={"verify_signature": False})  # Ignore signature verification for debugging
print(decoded)
from datetime import datetime

timestamp = 1740121313  # Replace with the decoded 'exp' value
expiry_time = datetime.utcfromtimestamp(timestamp)
print(expiry_time)


