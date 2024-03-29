# To install flask run: pip install flask
from flask import Flask, request, jsonify, send_file

#-------- Define classes that will be serialized
class ReflectorSimple:
    def __init__(self,data,ip,useragent):
        self.object = "Reflector Simple"
        self.userdata = data
        self.sourceip = ip
        self.useragent=useragent

    def getDict(self):
        return self.__dict__

class ReflectorJson:
    def __init__(self,data,json,ip,useragent):
        self.object = "Reflector Json"
        self.userdata = data
        self.value1 = json["value1"]
        self.value2 = json["value2"]
        self.sourceip = ip
        self.useragent=useragent

    def getDict(self):
        return self.__dict__
#--------------------------------------------

app = Flask(__name__)

# Show the REST APIs supported and format as a basic HTML. 
# When the main page is visited via browswer this page will be shown
@app.route('/')
def main():
    text = "<h3>Welcome to Copilot for Security test REST APIs. Please use the following REST API routes to get specific JSON results.</h1>"
    text += "<p><b> - GET /simple/&lt;data&gt; - Will return a JSON contains &lt;data&gt and few other fields </b>"
    text += "<p><b> - GET /params/&lt;data&gt; - Will return a JSON contains &lt;data&gt and few other fields passed in URL Params</b>"
    text += "<p><b> - POST /json/&lt;data&gt; - Will return a JSON contains &lt;data&gt and few other fields passed in payload JSON</b>"
    return text  

# ---------------- GET methods
@app.route('/simple/<data>', methods=['GET'])
def get_simple(data):
    obj = ReflectorSimple(data,getIpAddr(request),request.user_agent.string)
    response =  jsonify(obj.getDict())
    return response

@app.route('/params/<data>', methods=['GET'])
def get_params_data(data):
    args = request.args
    jsonData = args
    obj = ReflectorJson(data,jsonData,request.remote_addr,request.user_agent.string)
    response =  jsonify(obj.getDict())
    return response

# ---------------- POST methods
@app.route('/json/<data>', methods=['POST'])
def get_json(data):
    jsonData = ""
    if(request.is_json):
        try:
            # Handle Error
            jsonData = request.get_json(force=True) #request.json
            print("Received JSON:",jsonData)
        except Exception as e:
            print("Error",e)
            print("Request Content", str(jsonData))
            result = {'Error': "'" + str(e) + "'"}
            return result, 400 # Return error as HTTP 400
    obj = ReflectorJson(data,jsonData,request.remote_addr,request.user_agent.string)
    response =  jsonify(obj.getDict())
    return response


#---- OPTIONAL: Use this URL to return YAML files if you do not want to the host the files in FTP/Azure/Blob
#---- NOTE: All files should be placed in the ./Files folder 
@app.route('/file/<fileName>')
def get_file(fileName):
    try:
        filePath = 'Files\\'+fileName
        return send_file(filePath,download_name=fileName,as_attachment=True)
    except Exception as e:
        return str(e)

# Private function to return IP Address
def getIpAddr(request):
    if request.headers.getlist("X-Forwarded-For"):
        ip_addr = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_addr = request.remote_addr
    return ip_addr

if __name__ == '__main__':
    # Specify Network interface to bind to and the port to run
    app.run(host='0.0.0.0', port=5000)
    


