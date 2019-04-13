import urllib.request

url = 'http://localhost:8080/status/handler'
def handleTrainStep(url, id, step):
    headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    values = {
        "id": id,
        "step": step
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    res = urllib.request.urlopen(request).read().decode('utf-8')
    print(res)
