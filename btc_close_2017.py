from __future__ import (absolute_import, division, print_function, unicode_literals)

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import json

json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
response = urlopen(json_url)#返回一个http response abject

#print(response)
req = response.read()#req是一种byte编码方式  这种编码方式可以直接写入文件
#print(req)
with open('btc_close_2017_urllib.json', 'wb') as f:#b就是byte字节
    f.write(req)
#加载json格式
file_urllib = json.loads(req)
print(file_urllib)
print(type(file_urllib))
