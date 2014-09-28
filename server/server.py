from pexpect import pxssh
from flask import Flask, request, g, render_template, redirect
from parse import parse, parse_stats, parse_assignment_list, parse_all_grades
import json

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
	  
	    text_file = open("output.txt","w")
	    text_file.write(ret)
	    text_file.close()

	    s.logout()
	    return None

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
	  
	    text_file = open("output1.txt","w")
	    text_file.write(ret)
	    text_file.close()

	    s.logout()
	    return None

@app.route('/api/1')
def api1():
	username = request.args.get('username')
	password = request.args.get('password')
	callback = request.args.get('callback')

	go1(username, password)
	dict1, dict2, dict3, stats, dist = parse(ret)
	
	dict1 = (json.dumps(dict1))
	dict2 = (json.dumps(dict2))
	dict3 = (json.dumps(dict3))

	stats = (json.dumps(stats))
	dist = (json.dumps(dist))
	lst = [dict1, dict2, dict3, stats, dist]

	return callback + "(" + json.dumps({'data': lst}) + ")"

@app.route('/api/2')
def api2():
	username = request.args.get('username')
	assignment = request.args.get('assignment')
	callback = request.args.get('callback')
	password = request.args.get('password')
	
	go2(username, password, assignment)
	ret = open('output1.txt').read()

	stats = parse_stats(ret)

	return callback + "(" + json.dumps(stats) + ")"

if __name__ == "__main__":
    app.run()