import requests
import os,sys
import termcolor as tm
import socket
from datetime import datetime
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from tqdm import tqdm
import subprocess
import shutil



class Utils:
	def __init__(self,target_url):
		self.none = ''
		self.t_url = target_url
		self.u_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
		self.d_uri = self.t_url.split("://")[1]
		self.subdomains = list()
		self.directories = list()
		self.completed_counter = 0
		self.wordlist_size = 0

	def set_w_size(self,wsize):
		self.wordlist_size = wsize

	def write_subs_to_file(self):
		try:
			if os.path.exists(f"Data/{self.d_uri}"):
				if os.path.exists(f"Data/{self.d_uri}/subds"):
					shutil.rmtree(f"Data/{self.d_uri}/subds")
					os.mkdir(f"Data/{self.d_uri}/subds")
				else:
					os.mkdir(f"Data/{self.d_uri}/subds")
			else:
				os.mkdir(f"Data/{self.d_uri}")
				os.mkdir(f"Data/{self.d_uri}/subds")
		except Exception as EX:
			pass
		with open(f"Data/{self.d_uri}/subds/subdom.txt","w") as subd:
			for doms in self.subdomains:
				subd.write(str(doms)+"\n")

	def write_dirs_to_file(self):
		try:
			if os.path.exists(f"Data/{self.d_uri}"):
				if os.path.exists(f"Data/{self.d_uri}/dirs"):
					shutil.rmtree(f"Data/{self.d_uri}/dirs")
					os.mkdir(f"Data/{self.d_uri}/dirs")
				else:
					os.mkdir(f"Data/{self.d_uri}/dirs")
			else:
				os.mkdir(f"Data/{self.d_uri}")
				os.mkdir(f"Data/{self.d_uri}/dirs")
		except Exception as EX:
			pass
		with open(f"Data/{self.d_uri}/dirs/directories.txt","w") as subd:
			for dirs in self.directories:
				subd.write(str(dirs)+"\n")

	def Fetch_js(self):
		buffer_size = 1024 # Bytes
		d_uri = self.t_url.split("://")[1]
		timestamp = datetime.now()
		file = str(timestamp.year)
		file+= "-"+str(timestamp.month)+"-"+str(timestamp.day)+"-"+str(timestamp.hour)+"-"+str(timestamp.minute)+"-"+str(timestamp.second)
		with requests.session() as rsq:
			rsq.headers["User-Agent"] = self.u_agent
			try:
				if os.path.exists(f"Data/{d_uri}"):
					if os.path.exists(f"Data/{d_uri}/js"):
						shutil.rmtree(f"Data/{d_uri}/js")
					else:
						pass
				else:
					os.mkdir(f"Data/{d_uri}")

			except Exception as e:
				pass
			try:
				html = rsq.request(method="GET",url=self.t_url,allow_redirects=True,verify=True)
			except Exception as e:
				print("[-] Connection Failed!!!")
			soup_obj = bs(html.content, "html.parser")
			js_files = []
			js_url = ""
			for scr in soup_obj.find_all("script"):
				if scr.attrs.get("src"):
					if "://" not in str(scr.attrs.get("src")):
						js_url = urljoin(self.t_url,scr.attrs.get("src"))
					else:
						js_url = scr.attrs.get("src")
					js_files.append(js_url)
			os.mkdir(f"Data/{d_uri}/js")
			with requests.session() as rq:
				rq.headers["User-Agent"] = self.u_agent
				for urls in js_files:
					resp = rq.request(method="GET",url=urls.strip(),allow_redirects=False,verify=True)
					file_size = int(resp.headers.get("Content-Length",0))
					file_name = urls.split("/")[-1]
					#progress = tqdm(resp.iter_content(buffer_size),f"[*] Downloading {file_name}",total=file_size,unit="B",unit_scale=True,unit_divisor=1024)
					print("[*] Downloading %s" % file_name+" ....................!!!")
					download_instance = subprocess.Popen(["wget",f"{urls}","-O",f"Data//{d_uri}//js//{file_name}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					log_file = "wget-log"
					try:
						for f in os.listdir():
							if log_file in f:
								os.remove(f)
					except Exception as e:
						pass


	def Subdomain_enum(self,subd):
		subdom = subd+"."+self.t_url.split("://")[1]
		sock_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			ip = socket.gethostbyname(subdom)
			print(tm.colored(subdom,"magenta")+f" {tm.colored('has address','green')} "+tm.colored(ip,'yellow'))
			self.subdomains.append(subdom)
		except Exception as e:
			pass

	def Dir_enum(self,di):
		timestamp = datetime.now()
		event_time = str(timestamp.hour)+":"+str(timestamp.minute)+":"+str(timestamp.second)
		with requests.session() as dirq:
			dirq.headers["User-Agent"] = self.u_agent
			try:
				direq = dirq.request(method="GET",url=self.t_url+"/"+str(di),allow_redirects=False,verify=True)
				status_code = direq.status_code
				size = int(direq.headers.get("Content-Length",0))
				self.completed_counter +=1
				if int(size) < 1024:
					size = str(size)+"B"
				elif int(size) >= 1024:
					size = "%.2fKB"%float(int(size)/1024)
				else:
					pass
				if int(status_code) == 200: 
					print(tm.colored(f"[{event_time}] 200 -> {size} -> {di}","green"))
					self.directories.append(str(self.t_url+"/"+str(di)+str(" -> 200")))
				elif int(status_code) == 301:
					print(f"[{event_time}] 301 -> {size} -> {direq.headers.get('location',0)}")
					self.directories.append(str(self.t_url+"/"+str(di)+str(" -> 301")))
				elif int(status_code) == 403:
					print(tm.colored(f"[{event_time}] 403 -> {size} -> {di}","blue"))
				elif int(status_code) == 401:
					print(tm.colored(f"[{event_time}] 401 -> {size} -> {di}","red"))
					self.directories.append(str(self.t_url+"/"+str(di)+str(" -> 401")))
				else:
					pass
			except Exception as e:
				print("[-] Connection Failed!!!")
				pass
		if int(self.completed_counter) == int(self.wordlist_size):
			print("[*] Wordlist Exhausted!!!!")
			sys.exit()
		#if int(self.wordlist_size) - int(self.completed_counter) == 0 or int(self.wordlist_size) - int(self.completed_counter) == 1:
			#print("[*] Wordlist Exhausted!!!!")
			#sys.exit()
