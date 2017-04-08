import requests

USER_AGENT = 'Mozilla/5.0'
LOGIN_URL = 'https://leetcode.com/accounts/login/'
           
def login(username, password):
    headers = {
        'User-Agent': USER_AGENT,
        'Referer': LOGIN_URL
    }

    s = requests.Session()
    s.get(LOGIN_URL)
    csrftoken = s.cookies['csrftoken']

    payload = {'csrfmiddlewaretoken': csrftoken,
               'login': username,
               'password': password}
    s.post(LOGIN_URL, data=payload, headers=headers)
    return s
