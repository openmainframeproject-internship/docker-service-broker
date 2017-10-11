from flask import Flask, render_template, request
import subprocess
from OpenSSL import SSL
import sqlite3

app = Flask(__name__)

db = sqlite3.connect("serviceBrokerWeb.db")
c = db.cursor()

def runCMD(cmd):
    l = subprocess.check_output(cmd.split(" "))
    return l

def action(serviceData):
    if serviceData[1] == "CMD":
	return runCMD(serviceData[0])
    else:
	return False

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
	c.execute("select service_name from services")
        serviceData = list(c.fetchall())
	for i in range(0, len(serviceData)):
	    serviceData[i] = serviceData[i][0]
        return render_template("test.html", services=serviceData)
    else:
	c.execute("select service_command, service_type from services where service_name=?", [request.form['docker']])
	serviceData = c.fetchone()
        return request.form['docker']+" ran successfully and output was "+action(serviceData)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
