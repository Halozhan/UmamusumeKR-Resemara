import urllib.request

def internet_on():
    try:
        urllib.request.urlopen("http://google.com", timeout=3)
        return True
    except:
        return False

print(internet_on())