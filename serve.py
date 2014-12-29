import json
import web
from iperfhandle import IperfTcp


urls = ('/index', 'Index',
        '/getlist.json', 'Getlistjson')

render = web.template.render('templates')

tcplist = []

class Getlistjson:
    def GET(self):
        mydict = {'one':1, 'two':2}
        web.header('Content-Type', 'application/json')
        return json.dumps(mydict)

class Index:
    def GET(self):
        return render.myperf()

        #return """<html><head></head><body>
#<form method="POST" enctype="multipart/form-data" action="">
#<input type="file" name="myfile" />
#<br/>
#<input type="submit" />
#</form>
#</body></html>"""


if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()

