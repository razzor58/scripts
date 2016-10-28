#Import libs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
import subprocess
import ConfigParser
import ftputil
import time
import smtplib
import os   

#Define user functions
def get_conf(parameter):
 try:
	config = ConfigParser.ConfigParser()
	config.read("conf.ini")
 except Exception as err:	
	print_log("read error: " + str(err))       
 return config.get("main", parameter)


def print_log(log_data):
 try:
	with open('upload.log', 'a') as log_file:	
	 log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + " >> " + log_data + "\n")		
 except Exception as err:	
	print_log("log file write error: " + str(err))
       
def go_to_ftp():
 try:
	command_list=[]
	file_list=[]
	objects_to_process = {"files":file_list,"commands":command_list}
	print_log("go to ftp")
	with ftputil.FTPHost(get_conf("ftp_address"), get_conf("ftp_user"), get_conf("ftp_user")) as host:
		host.chdir(get_conf("ftp_dir"))
		for item in host.listdir(host.curdir):
		  	if "get_" in item:
  				command_list.append(item)
		  		host.remove(item)
 			if ".csv" in item:
		  		file_list.append(item)
		  		host.download(item,item)
		  		host.remove(item)	  		
 except Exception as err:	
	print_log("ftp error: " + str(err)) 
 return objects_to_process
	
def db_load_file(ree,ftype):
 try:  
	print_log("load " + ree)       	
	data_file = open(str(ftype) + ".dat", "w")
	upload_file = open(ree,"r")
	data_file.write(upload_file.read())
        subprocess.call("sqlldr " + get_conf("connection_string") + " control=" + ftype + ".ctl", shell=True)
	if ftype+".bad" in listdir:
		send_mail(get_conf("fail_load_subj"),get_conf("fail_load_body"))
		os.remove(ftype + ".bad")
	else:
		send_mail(get_conf("sucsess_load_subj"),get_conf("sucsess_load_body"))	 
		os.remove(ftype + ".log")
 except Exception as err:	
	print_log("load file error: " + str(err))
        
def make_report(report_name):
 try:   
	subprocess.call("sqlplus " + get_conf("connection_string") + " @" + report_name + ".sql", shell=True)
	send_mail(subj = get_conf(report_name))
 except Exception as err:	
	print_log("make report error: " + str(err))        
 
def send_mail(subj):
 try:
	fp = open("result.txt", 'rb')
	msg = MIMEText(fp.read())
	fp.close()
	msg["Subject"] = subj
	msg["From"] = get_conf("mail_sender")
	msg["To"] = get_conf("mail_receiver")
	s = smtplib.SMTP("localhost")
	s.sendmail(get_conf("mail_sender"),get_conf("mail_receiver"),msg.as_string())
	s.quit()
 except Exception as err:	
	print_log("mail sending error: " + str(err))        
##########################################################################################
## MAIN PROGRAM                                                                                          
##########################################################################################
try:
#define allowed actions
 load_types = ("contr","dist")
 report_commands = ("get_nsi","get_dist","get_contr","get_nsi_all")
 print_log("start ")
#get dict with actions from ftp
 process_data = go_to_ftp()
#Process files
 for ree in process_data["files"]:
	if ree.split("_")[0] not in load_types:
	   print_log(ree + "file skip")
	else:	
	 db_load_file(ree,ree.split("_")[0])
#Process commands
 for report in process_data["commands"]:
	if report.split(".")[0] not in report_commands:
	   print_log(report + "file skip")
	else:	
	 make_report(report.split(".")[0])
except Exception as err:	
 print_log("error in main program:  " + str(err))        
finally:
 print_log("end") 

       