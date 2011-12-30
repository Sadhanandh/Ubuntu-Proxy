#!/usr/bin/python
#  This is a tool to automatically configure system-wide proxy settings in Ubuntu 
#  Its an invaluble script to configure proxies with username and password especially in universities and companies
#  which eliminates the need of repetitive editing of system files which is prone to frequent manual errors	
#  You need to be a root user to run this script.
#  For further information you may use -I option 
#	
#
#	Author: Sadhanandh Vishwanath
#
#	Profile: http://goo.gl/IVg3g
#
#	E-mail: sadhanandhiyer[@]gmail[.]com
#
#	Date: 9/25/2011
# 
#"""With power comes responsibility, so use 'sudo' with care"""

filenames=["/etc/bash.bashrc","/etc/environment"]
filename2="/etc/apt/apt.conf"
logs="/var/log/proxychangerlog"    

def filewrite2(srv,port):
    lin=[]
    typ0 = ("http","ftp","https")
    for filenam in filenames:
        fil = open(filenam,"a")
        for x in typ0:
			if (filenam.find("bash")!=-1) :
				lin.append("export %s_proxy=\"%s://%s:%s\"\n" % (x,x,srv,port))
			else:	
				lin.append("%s_proxy=\"%s://%s:%s\"\n" % (x,x,srv,port))
        for l in lin:
            fil.write(l)
        fil.close()
        lin=[]


    lin2=[]
    fil = open(filename2,"w")
    for x1 in typ0:
        lin2.append('Acquire::%s::proxy "%s://%s:%s/";\n' %(x1,x1,srv,port))    
    for l1 in lin2:
        fil.write(l1)
    fil.close()

def filewrite4(srv,port,name,pasw):
    lin=[]
    typ0 = ("http","ftp","https")
    for filenam in filenames:
        fil = open(filenam,"a")
        for x in typ0:
			if (filenam.find("bash")!=-1):
				lin.append("export %s_proxy=\"%s://%s:%s@%s:%s\"\n" % (x,x,name,pasw,srv,port))
			else:	
				lin.append("%s_proxy=\"%s://%s:%s@%s:%s\"\n" % (x,x,name,pasw,srv,port))
        for l in lin:
            fil.write(l)
        fil.close()
        lin=[]


    lin2=[]
    fil = open(filename2,"w")
    for x1 in typ0:
        lin2.append('Acquire::%s::proxy "%s://%s:%s@%s:%s/";\n' %(x1,x1,name,pasw,srv,port))    
    for l1 in lin2:
        fil.write(l1)
    fil.close()

def backup(files):
	for fil in files:
		try:
			f1=open(fil,"r")
			l=f1.read()
			f1.close()
			if(fil.find(".")==-1):
				newname=fil+".backup"
			else:
				newname=fil[:fil.find(".")]+".backup"
			f2=open(newname,"w")
			f2.write(l)
			f2.close()
		except :
			pass

def clean(file2,files,para=False):
	if(para):
		for file1 in files:
			try:
				f=open(file1,'r')	
				l = f.read()
				l = re.sub(r'\n?(.*http_proxy\s*=\s*".*")',r'\n# \g<1>',l)
				l = re.sub(r'\n?(.*https_proxy\s*=\s*".*")',r'\n# \g<1>',l)
				l = re.sub(r'\n?(.*ftp_proxy\s*=\s*".*")',r'\n# \g<1>',l)
				f.close()
				f=open(file1,'w')
				f.write(l)
				f.close()
			except:
				f.close()
				sys.exit(1)
	else:
		for file1 in files:
			try:
				f=open(file1,'r')
				l = f.read()
				l = re.sub(r'\n?(.*http_proxy\s*=\s*".*")',r'\n',l)
				l = re.sub(r'\n?(.*https_proxy\s*=\s*".*")',r'\n',l)
				l = re.sub(r'\n?(.*ftp_proxy\s*=\s*".*")',r'\n',l)
				f.close()
				f=open(file1,'w')
				f.write(l)
				f.close()
			except:
				f.close()
				sys.exit(0)
		try:		
			f=open(file2,"r")
			l = f.read()
			l = re.sub(r'\n?(.*Acquire.*".*?";)' ,"",l)		
			f.close()
			f=open(file2,'w')
			f.write(l)
			f.close()
		except:
			f.close()
			sys.exit(1)

import re
import sys
from datetime import datetime
try:
	flog=open(logs,"a")
	flog.write(str(datetime.now())+"\n")
except:
	print "Are you the root user? Please try again as root user ie. use sudo command"
	print "Eg ->     sudo %s -h" %sys.argv[0]
	flog.write("You are not the super user \n")
	flog.close()
	sys.exit(1)	
if(len(sys.argv)<2):
		print "Use Options----"
		print "Type sudo %s -h for help " % sys.argv[0]
else:
	backup([filenames[0],filenames[1],filename2])
	flog.write("Files have been backed up in the same location with .backup extension \n")
	if(sys.argv[1]=="-I"):
		print "Hello"
		print "This is a script to change or delete network proxy"
		print "To make it an executable ->"
		print "sudo chmox +x %s" %sys.argv[0]
		print "\n"
		print "Eg. syntax to edit network proxy with username 'myname' and password 'mypassword' will be -> "
		print "sudo %s -A 192.168.1.1 4112 myname mypassword" % sys.argv[0]
		print "presuming that your proxy server exists on the IP - 192.168.1.1"
		print "and your port is -4112"
		print "your username is -myname"
		print "your password is -mypassword"
		print "\n"
		print "If your proxy consists only of an IP and port use -P option"
		print "\n"
		print "To remove any proxy configuration that may have been made earlier use -R option" 
	elif(sys.argv[1]=="-h"):
		print "Help Options...."
		print "-I for Information"
		print "-P for Proxy "
		print "-A for Authorization -username and pass"
		print "-R for Removing proxy"
		print "-C for Changing profile" 
	elif(sys.argv[1]=="-P"):
		if(len(sys.argv)<4):
			print "Error: You must use an option such as... %s -P ProxyIP Port" % sys.argv[0]
			print "For Eg . %s -P 192.168.1.1 4112" % sys.argv[0]
		else :
			filewrite2(sys.argv[2],sys.argv[3])
			flog.write("2 var proxy changed \n")
			print "Make sure you don't require authentication. Your proxy settings have been changed successfully."
			
	elif(sys.argv[1]=="-A"):
		if(len(sys.argv)<6):
			print "Error: You must use an option such as... %s -A ProxyIP Port Username Password" % sys.argv[0]
			print "Eg . %s -A 192.168.1.1 4112 username password" % sys.argv[0]
		else:
			filewrite4(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
			flog.write("4 var.proxy changed \n")
			print "Your proxy settings have been changed and authentication configuration set as per the provided information."

	elif(sys.argv[1]=="-R"):
		clean(filename2,filenames)
		flog.write("Old proxy removed \n")
		print "All your previously configured proxy settings have been cleared."
	
	elif(sys.argv[1]=="-C"):
		if(len(sys.argv)<3):
			print "Error: You must use an option such as like %s -C profile_number" % sys.argv[0]
			print "Eg %s -C 1" % sys.argv[0]
		else:
			print "Will be implemented soon ....... Check out the repository"
	else:
		print "Oops! This is an unknown option -- Please try -h to know all the available options"

flog.close()
