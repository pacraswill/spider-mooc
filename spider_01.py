import urllib.request
import ssl
import re


def get_html(url):
    context = ssl._create_unverified_context()
    page = urllib.request.urlopen(url, context=context).read()
    html = bytes.decode(page)
    return html


reg = r'src="(.+?\.jpg)"'
reg_img = re.compile(reg)
imglist = reg_img.findall(get_html('https://www.meituri.com/a/13472/'))
x = 0
for img in imglist:
    urllib.request.urlretrieve(img, "%s.jpg" % x)
    x += 1
