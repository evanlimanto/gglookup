from pexpect import pxssh
from flask import Flask, request, g, render_template, redirect

app = Flask(__name__)

def go1(username, password):
	s = pxssh.pxssh()
	if not s.login ('cory.eecs.berkeley.edu', username, password):
	    print ("SSH session failed on login.")
	else:
	    print ("SSH session login successful")
	   
	    commands = ["glookup -t", "glookup", "glookup -s Total"]
	    ret = ""
	   
	    for tmp in commands:
	    	print(tmp)
	    	s.sendline(tmp)
	    	s.prompt()
	    	
	    	str = s.before
	    	str = str.decode()
	    	ret += str
	    
	    ret = ret.replace('glookup -t','')
	    ret = ret.replace('glookup -s Total','')
	    ret = ret.replace('glookup','')
	    
	    ret = ret.replace('\\r\\n','\n')
	  
	    # text_file = open("output.txt","w")
	    # text_file.write(ret)
	    # text_file.close()

	    s.logout()
	    return "{\"data\":\"" + ret + "\"}"

def go2(username, password, assignment):
	s = pxssh.pxssh()
	if not s.login ('cory.eecs.berkeley.edu', username, password):
	    print ("SSH session failed on login.")
	else:
	    print ("SSH session login successful")
	   
	    commands = ["glookup -s " + assignment]

	    ret = ""
	   
	    for tmp in commands:
	    	print(tmp)
	    	s.sendline(tmp)
	    	s.prompt()
	    	
	    	str = s.before
	    	str = str.decode()
	    	ret += str
	    
	    ret = ret.replace('glookup -s ' + assignment,'')
	    
	    ret = ret.replace('\\r\\n','\n')
	  
	    # text_file = open("output.txt","w")
	    # text_file.write(ret)
	    # text_file.close()

	    s.logout()
	    return "{\"data\":\"" + ret + "\"}"


@app.route('/api/1')
def api1():
	username = request.args.get('username')
	password = request.args.get('password')
	password = "Im2afn9tIm2afn9t"

	return go1(username, password)

@app.route('/api/2')
def api2():
	username = request.args.get('username')
	password = request.args.get('password')
	assignment = request.args.get('assignment')
	password = "Im2afn9tIm2afn9t"

	return go2(username, password, assignment)

if __name__ == "__main__":
    app.run()