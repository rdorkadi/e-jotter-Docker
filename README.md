# e-jotter

Minimal Note Taking App with Multi-factor Autentication enabled



# Run the app on Docker

1. Pull the docker image from docker hub

```
# docker pull riyadorkadi/e-jotter-amd64
```

2. Run the docker image (on arm64 (ie., Mac M1, M2))

```
docker run --name fnote-mfa-cont01 -dit -p 5001:5001 riyadorkadi/e-jotter-amd64:latest
```

To run docker image on amd64 or x86_64 (ie., On AWS EC2, Intel etc)

```
docker run --name fnote-mfa-cont01 -dit -p 5001:5001 riyadorkadi/e-jotter-amd64:latest
```

Check dockerhub for more details: https://hub.docker.com/riyadorkadi/e-jotter-amd64

3. Open the app in browser

```
http://localhost:5001/
```

# To run locally 

1. Clone this repo 

2. Create a virtual environment and install the dependent packages

```
# virtualenv venv

# source venv/bin/activate

# pip3 install -r requirements.txt

# python3 main.py
```

## Sample images

![Signup Page Blank](images/Sign_up_page.png "Sign Up Page")

![Signup Page Filled](images/Login_page.png "Login Page")

![MFA QR Page](images/MFA_Scan_Page.png "MFA QR Code")

![Login Page](images/Successful_loggedIn_page.png "Successfully Logged In Page")

![Home Page](images/Notes_page.png "Authentic user's home page containing notes")

## Functionalities

- Create a new user (Signup)
- Multi-factor Authentication (Using TOPT)
- Login only for signed up user (Login and Logouts)
- Create notes (NOT shared notes, each user can only see his notes)
- Delete notes (Only registerd users can delete/create notes)
- Cannot see other users notes
