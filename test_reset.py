import urllib.request
import urllib.parse
import http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Register
print("Registering...")
data = urllib.parse.urlencode({
    'name': 'Reset Test Corp',
    'registration_no': '999888',
    'email': 'reset2@testcorp.com',
    'password': 'password123'
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:5000/company/register', data=data)
try:
    resp = opener.open(req)
    print("Registration OK")
except urllib.error.HTTPError as e:
    print("Registration Failed", e.code)

# 2. Hit the Reset Data route
print("Hitting reset data...")
req = urllib.request.Request('http://127.0.0.1:5000/company/reset-data', data=b'')
try:
    resp = opener.open(req)
    html = resp.read().decode('utf-8')
    print("Reset OK")
    if 'All test data and requests have been successfully cleared' in html:
        print("Success message found!")
    else:
        print("Success message NOT found.")
except urllib.error.HTTPError as e:
    print("Failed to reset:", e.code)
