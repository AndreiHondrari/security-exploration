# CSRF / XSRF (Cross-Site Request Forgery)

## Description

In a CSRF attack, requests to a resource that requires authentication are bypassed by performing the attack from the client's browser. In this experiment these components are required:
- a server with login, logout and a session-protected endpoint
- an official website page
- a website with a forged form that performs the malicious request to the server

How this works is that the target client must be already authenticated with the server, hence there is a session active. If this prerequisite is fulfilled then the attacker can manipulate the target to open the page with the forged form. What happens is that the moment the victim opens that page, the form automatically submits by means of an on-load JavaScript call. The form gets submitted, and the server acknowledges it as being a valid request, since the session is valid. The reason why this happens is that the browser sends any request to an URL, with it's browser associated session, no matter where the request is made from.

## What you need to run this demo
- Install flask

## How to run this demo
- Execute `./main.py` -> should open a http://localhost:5000 (runs a flask dev server)
- Open http://localhost:5000 and login with the provided username and password (it's hinted in the page `myuser` and `1234`)
- If you opened the server with a different domain and port other than `localhost` and `5000`, make sure to open `hacked.html` and edit the `action="http://yourdomain:yourport"` of the form.
- When you open hacked.html with your browser, it will automatically submit to your server in a malicious and unverified manner -> this demonstrates the vulnerability. If you check the server console you will see that the server logged `POSTMESSAGE: MALICIOUS MESSAGE !!!` as proof. In a secure environment it shouldn't have been possible to get to this point.

## Ways to counteract
- CSRF token
- SameSite cookies
