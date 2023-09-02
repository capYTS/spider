import urllib3

http = urllib3.PoolManager()
url = 'https://read.douban.com/j/kind/'
header=
response = http.request("GET", url, headers=header)
repsonString = response.data.decode("utf-8")
