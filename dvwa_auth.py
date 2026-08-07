import requests
from bs4 import BeautifulSoup

def get_dvwa_session(base_url="http://localhost/DVWA/", username="admin", password="password"):
    session = requests.Session()

    login_page = session.get(base_url + "login.php")
    soup = BeautifulSoup(login_page.text, "html.parser")
    token_input = soup.find("input", {"name": "user_token"})
    user_token = token_input["value"] if token_input else ""

    login_data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": user_token,
    }
    session.post(base_url + "login.php", data=login_data)

    return session

def set_security_low(session, base_url="http://localhost/DVWA/"):
    page = session.get(base_url + "security.php")
    soup = BeautifulSoup(page.text, "html.parser")
    token_input = soup.find("input", {"name": "user_token"})
    user_token = token_input["value"] if token_input else ""

    session.post(base_url + "security.php", data={
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": user_token,
    })

if __name__ == "__main__":
    session = get_dvwa_session()
    resp = session.get("http://localhost/DVWA/vulnerabilities/sqli/")
    if "User ID" in resp.text:
        print("LOGIN SUCCESS - can see SQLi page")
    else:
        print("LOGIN FAILED - still blocked")
        print(resp.text[:500])