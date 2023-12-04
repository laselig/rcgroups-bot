from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from datetime import datetime
from pytz import timezone
# from twilio.rest import Client
# from requests_ip_rotator import ApiGateway, EXTRA_REGIONS

import time, random, smtplib, requests
from fake_useragent import UserAgent
# from requests_ip_rotator import ApiGateway





ACCESS_KEY = "AKIAVH75IAV62FZGFFMK"
SECRET_KEY = "8oOjTJ3oWMA9MUVU/yUlaYbUt+yGCd7p7lkmecoZ"

# from proxy_requests import ProxyRequests



airplanes = "https://www.rcgroups.com/aircraft-fuel-airplanes-fs-w-38/"
engines = "https://www.rcgroups.com/aircraft-fuel-engines-and-accessories-fs-w-362/"
fuel_jets = "https://www.rcgroups.com/aircraft-fuel-jets-fs-w-381/"
misc = "https://www.rcgroups.com/aircraft-general-miscellaneous-fs-w-306/"
free_flight = "https://www.rcgroups.com/aircraft-free-flight-and-control-line-fs-w-1065/"
sail = "https://www.rcgroups.com/aircraft-sailplanes-fs-w-100/"
electric = "https://www.rcgroups.com/aircraft-electric-airplanes-fs-w-15/"
fpv = "https://www.rcgroups.com/fpv-equipment-fs-w-710/"
radio = "https://www.rcgroups.com/aircraft-general-radio-equipment-fs-w-215/"

forums = [airplanes, engines, fuel_jets, misc, free_flight, sail, electric, fpv, radio]
account_sid = 'ACcda44ba0fa966b1e548eb4f5beabc9db'
auth_token = '440ea0f2b14f81f456c7e7d97f6f429c'
def get_terms(filename):
	with open(filename, "r") as f:
		lines = f.readlines()
		cleaned = []
		for line in lines:
			if("#" not in line):
				new = line.replace("\n", "").replace(" ", "-")
				if(new != ""):
					cleaned.append(new)
	return cleaned

def get_names(filename):
	with open(filename, "r") as f:
		lines = f.readlines()
		# print(lines)
		cleaned = []
		for line in lines:
			if("#" not in line):
				new = line.replace("\n", "")
				if(new != ""):
					cleaned.append(new)
	return cleaned

def save(filename, val):
	with open(filename, 'w') as f:
		f.write(str(val))

def load(filename):
	with open(filename, 'r') as f:
		return int(f.read())

def read_config(filename):
	hash = {}
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			splitted = line.split("=")
			if(len(splitted) == 2):
				variable = splitted[0].strip()
				val = int(splitted[1].strip())
				hash[variable] = val

	return(hash)

def read_ips(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()
	return lines


# def send_request(session, proxy, url):
#    try:
#        response = session.get(url, proxies={'http': f"http://{proxy}"})
#        print(response.json())
#    except:
#        pass
def proxy_request(url):
	print(url)

	# gateway = ApiGateway("https://rcgroups.com", ACCESS_KEY, SECRET_KEY, region="us-east-1")
	# gateway.start()
	# session = requests.Session()
	# session.mount("https://rcgroups.com", gateway)
	# response = requests.get(url)
	# print (response.status_code)
	# return response.text

	ua = UserAgent()

	import subprocess
	while(True):
		fake_ip = random.choice(read_ips("http_proxies.txt")).strip()
		print("Trying", fake_ip)
		try:
			result = subprocess.run(
				["curl", "-x", fake_ip, "-v", url],
				capture_output=True)
			print(result)
			return str(result.stdout)
		except:
			pass


# print(result)
	# print(result.stdout)




def extract_price(price):
	nums = [str(x) for x in range(0, 10)] + ["."]
	buffer = ""
	for char in price:
		if(char in nums):
			buffer += char

	return(float(buffer) if buffer != "" else 1000000)

def build_forums_list(config):
	forums = [airplanes, engines, fuel_jets, misc, free_flight, sail, electric, fpv, radio]

	if(config["search_Sail"] == 0):
		forums.remove(sail)
	if(config["search_Misc"] == 0):
		forums.remove(misc)
	if(config["search_FPV"] == 0):
		forums.remove(fpv)
	if(config["search_Fuel_jets"] == 0):
		forums.remove(fuel_jets)
	if(config["search_Free_flight"] == 0):
		forums.remove(free_flight)
	if(config["search_Electric"] == 0):
		forums.remove(electric)
	if(config["search_Engines"] == 0):
		forums.remove(engines)
	if(config["search_Airplanes"] == 0):
		forums.remove(airplanes)
	if(config["search_Radio"] == 0):
		forums.remove(radio)

	return(forums)
# search_terms = get_terms("keywords.txt")
# watchlist = get_terms("usernames.txt")



while(True):
	potential = []
	names = []
	prices = []
	search_terms = get_terms("keywords.txt")
	watchlist = get_names("usernames.txt")
	not_terms = get_terms("not_keywords.txt")
	not_watchlist = get_names("not_usernames.txt")

	config = read_config("scraper.config")
	forums = build_forums_list(config)
	max_price = float(config["ignore_PriceGreaterThan"])


	if(config["enable_BotSearch"] == 0):
		pass
		print("passing")
	else:
		for forum in forums:
			forum_short = forum.split("/")[-2]
			# ip_addresses = read_ips("http_proxies.txt")
			page = proxy_request(forum)
# 			page = session.get(forum)
# 			print(page)
# 			page = requests.get(forum)
			soup = BeautifulSoup(page, 'html.parser')
			titles = soup.find_all('tr', valign = "top")
			for t in titles:
				# print(t.text.strip())
				link = t.find('a')['href']
				link = link.split("&")
				link = link[0]
				link = link.lower()
				#get username
				uraw = t.find("span", style="font-weight:bold;")
				if(uraw == None):
					username = None
				else:
					username = uraw.text

				#get price
				price = t.find("div", {"class": "fsw-price-text"})
				if(price == None):
					price = t.find("div", {"class": "fsw-price-text-rcgplus"})
				if(price == None):
					price = "WTB"
				if(price != "WTB"):
					price = price.text.strip()

				shipping = t.find("div", {"class": "fsw-shipping"})
				if(shipping != None):
					shipping = shipping.text.strip()


				send_email = True
				for term in search_terms: # check link for all search terms
					#reason to send email
					if((term in link or username in watchlist) and forum_short not in link):
						if(link[0] == "/"):
							link = link[1:]
						full = forum + link
						print(full)

						# reasons to not send email
				# 		for not_term in not_terms:
				# 			if(not_term in link):
				# 				send_email = False
				# 		if(username in not_watchlist):
				# 			send_email = False
				# 		if(forum[-1] == "/" and link[0] == "/"):
				# 			send_email = False

				# 		if(send_email and extract_price(price) <= max_price and shipping != "Will not ship"):
				# 			potential.append(full)
				# 			names.append(username)
				# 			prices.append(price)
				# 			break

						if(send_email):
							potential.append(full)
							names.append(username)
							prices.append(price.replace("\\r", "").replace("\\n", "").replace("\\t", ""))
							break

		body_name = "Found the following links - sent from Heroku Web:\n"
		body = body_name
		print(body)
		with open("seen.txt", 'r') as seen:
			seen_threads = [a.strip() for a in seen.readlines()]

		with open("seen.txt", "a") as append:
			for i, link in enumerate(potential):
				# print(i)
				if(link not in seen_threads):
					append.write(link + "\n")
					try:
						name = names[i].encode('ascii', 'ignore').decode('ascii')
						price = prices[i].encode('ascii', 'ignore').decode('ascii')

						try:
							why = '-'.join(link.split("?")[1].split('-')[1:])
						except:
							why = "Parsing error"
						main_forum = "/".join(link.split("//")[1].split("/")[:2])
						body += why + " -- " + str(price) + "\nhttps://" + main_forum + "\n" + link + "\n" + str(name) + "\n\n\n"
					except:
						print("name or price is None")
						continue



		if(body != body_name):
			central = timezone('US/Central')
			ct_time = datetime.now(central)
			timestr = ct_time.strftime("%m/%d/%Y, %H:%M:%S")
			counter = load("counter.txt")

			message_body = body + "\n" + timestr + "\n" + "Messages sent: " + str(counter)
			counter += 1
			save("counter.txt", counter)

			print("SENDING EMAIL")
			print(config["send_Email"])
			print(config["send_SMS"])
			if(config["send_Email"] == 1):
				msg = MIMEText(message_body)
				msg['Subject'] = "RC Groups -- Recent RC Groups Posts"
				msg['From'] = 'RC Groups Bot <rcgroupsbot@gmail.com>'
				msg['To'] = 'Michael Selig <michael@selig.com>'
				server = smtplib.SMTP("smtp.gmail.com", 587)
				server.starttls()
				server.login("rcgroupsbot@gmail.com", "sieuxgwcdssenfgo")
				server.sendmail("rcgroupsbot@gmail.com", "lucasaselig@gmail.com", msg.as_string())
				server.sendmail("rcgroupsbot@gmail.com", "mselig@alumni.princeton.edu", msg.as_string())
				server.quit()

			# if(config["send_SMS"] == 1):
			# 	message = client.messages.create(body=message_body, from_='+12058914969', to='+12176213057')
				# try:
				# 	message = client.messages.create(body=message_body, from_='+14437752520', to='+12176218804')
				# except:
				# 	print("Client has STOP on")
				# 	pass
		# testing
		#requests.get("https://m-selig.ae.illinois.edu/")
		#requests.get("https://www.inertiasoft.com/")


		rand_min = random.randint(3, 4)
		# time.sleep(60 * rand_min)
		# break
