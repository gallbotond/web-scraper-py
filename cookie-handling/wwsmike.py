import requests

# try to bypass detection by sending back all the cookies we get from the response
response = requests.get("https://www.emag.ro")

print(response.cookies)

# create a new request with the cookies we got from the previous response

n = 0
# request while response code is 200
while response.status_code == 200:
    response = requests.get("https://www.emag.ro", cookies=response.cookies)
    print(response.cookies)
    n += 1
    print(f"Number of requests: {n}")
