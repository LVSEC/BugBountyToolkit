from Core.Controllers import Utils as ut
import signal
import pyfiglet
import termcolor as tm
import sys
import socket
import concurrent.futures
from datetime import datetime
def sig_handler(received_sig, frame):
	print("\nCtrl-C detected, Exitting..................!")
	sys.exit()

signal.signal(signal.SIGINT,sig_handler)
def print_banner():
	figfont = 'smshadow' # you can list fonts by typing pyfiglet --list fonts
	figinit = pyfiglet.Figlet(font=figfont)
	banner = "BugBountyToolkit"
	print(tm.colored(figinit.renderText(banner),"yellow"))

def check_domain_validity(domain):
	dom = domain.split("://")[1]
	socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		ip = socket.gethostbyname(dom)
	except Exception as e:
		print("[-] "+tm.colored("Invalid domain!!!!","red"))
		sys.exit()

def validate_input(d):
	if "://" in d:
		pass
	else:
		print("[-] Host Scheme not found in the provided domain!!!")
		sys.exit(-1)

def validate_input_type(inp):
	valid_charset = "1234567890"
	inp = str(inp)
	inp_l = len(inp)
	index = 0
	while not index > int(inp_l) - 1:
		if inp[int(index)] in valid_charset:
			pass
		else:
			print("[-] Invalid Input, Please provide an Integer!!!")
			sys.exit(-1)
		index +=1
def main_menu():
	print_banner()
	domain = str(input(">>Domain_name:"))
	validate_input(domain)
	check_domain_validity(domain)
	init = ut(domain)
	print("1 -> "+tm.colored("Subdomain Enumeration","yellow"))
	print("2 -> "+tm.colored("Directory Enumeration","yellow"))
	print("3 -> "+tm.colored("JsFile Downloader","yellow"))
	print("4 -> "+tm.colored("Exit","red"))
	opt = input(">>Opt:")
	validate_input_type(opt)
	if int(opt) == 1:
		max_allowed_threads = 40
		threads_s = 0
		counter = 1
		while True:
			threads_s = input(">>Threads:")
			validate_input_type(threads_s)
			if int(threads_s) > max_allowed_threads:
				print("[-] "+tm.colored("Thread number could not exceed 40!!!","red"))
				continue
			elif int(threads_s) <= max_allowed_threads:
				break
			else:
				print("[-] "+tm.colored("Invalid literal!!!","red"))
				sys.exit()

		with open("dict/subdomains/Subdomain.txt") as subds:
			f_dats = subds.readlines()
			wordlist_size = len(f_dats)
			print("[*] "+tm.colored("Worldlist Size","yellow")+" -> {}".format(wordlist_size))
			print("[*] "+tm.colored("Threads","yellow")+" -> {}".format(threads_s))
			with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads_s)) as executor:
				tasks = []
				for dms in f_dats:
					#percentage = counter*100/wordlist_size
					executor.submit(init.Subdomain_enum,dms.strip())
					#print("[*] Progress %.2f"%percentage,end="\r")
			init.write_subs_to_file()
	elif int(opt) == 2:
		timestamp = datetime.now()
		event_time = str(timestamp.hour)+":"+str(timestamp.minute)+":"+str(timestamp.second)
		max_allowed_threads = 40
		threads_s = 0
		counter = 1
		while True:
			threads_s = input(">>Threads:")
			validate_input_type(threads_s)
			if int(threads_s) > max_allowed_threads:
				print("[-] "+tm.colored("Thread number could not exceed 40!!!","red"))
				continue
			elif int(threads_s) <= max_allowed_threads:
				break
			else:
				print("[-] "+tm.colored("Invalid literal!!!","red"))
				sys.exit()

		with open("dict/webcontent/dicc.txt") as dirs:
			f_dats = dirs.readlines()
			wordlist_size = len(f_dats)
			init.set_w_size(wordlist_size)
			print("[*] "+tm.colored("Worldlist Size","yellow")+" -> {}".format(wordlist_size))
			print("[*] "+tm.colored("Threads","yellow")+" -> {}".format(threads_s))
			print("[*] "+tm.colored("Target","yellow")+" -> {}".format(domain))
			print(tm.colored(f"[{event_time}] Starting:","yellow"))
			with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads_s)) as executor:
				tasks = []
				for di in f_dats:
					#percentage = counter*100/wordlist_size
					executor.submit(init.Dir_enum,di.strip())
					#print("[*] Progress %.2f"%percentage,end="\r")
			init.write_dirs_to_file()
	elif int(opt) == 3:
		init.Fetch_js()
	elif int(opt) == 4:
		sys.exit()
	else:
		print("[-] "+tm.colored("Invalid Opt!!!","red"))


if __name__ == "__main__":
	main_menu()