#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: EO-RIPPER.py                       ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#*******************************************

import random, re, string, urllib, urllib2, mechanize, cookielib, requests, json
from urllib2 import urlopen
from bs4 import BeautifulSoup
from pygoogle import pygoogle

emails_list = "emails.txt"

class colores:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    alert = '\033[93m'
    fail = '\033[91m'
    normal = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

br = mechanize.Browser()
cj = cookielib.LWPCookieJar() 
br.set_cookiejar(cj) 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def check_fb(email):
	#FACEBOOK-----------------------------------------------------
	r = br.open('https://www.facebook.com/login.php')
	br.select_form(nr=0)
	br.form["email"] = email
	br.form["pass"] = "123412341234"
	br.submit()
	respuestaFB = br.response().geturl()
	html = br.response().read()
	print "[INFO][FB][URL] " + respuestaFB
	soup = BeautifulSoup(html, "html.parser")
	for img in soup.findAll("img"):
		print img

def check_linkedin(email, state):
	try:
		#LINKEDIN-------------------------------------------------
		r = br.open('https://www.linkedin.com/')
		br.select_form(nr=0)
		br.form["session_key"] = email
		br.form["session_password"] = "123456"
		br.submit()
		respuestaURL = br.response().geturl()
		if "captcha" in respuestaURL:
			print "|--[INFO][LinkedIn][Captcha][>] Captcha detect!"
		else:
			pass
		html = br.response().read()
		#print "|--[INFO][LinkedIn][URL][>] " + respuestaLI
		soup = BeautifulSoup(html, "html.parser")
		for span in soup.findAll("span", {"class", "error"}):
			data = remove_tags(str(span))
			if "password" in data:
				print "|--[INFO][LinkedIn][CHECK][>] The account exist..."
				if state == 1:
					print colores.blue + "|--[INFO][LinkedIn][CHECK][>] it's possible to hack it !!!" + colores.normal
			if "recognize" in data:
				print "|--[INFO][LinkedIn][CHECK][>] The account doesn't exist..."
	except:
		print colores.alert + "|--[WARNING][LinkedIn][>] Error..." + colores.normal

def check_wordpress(email, state):
	try:
		r = br.open('http://wordpress.com/wp-login.php')
		br.select_form("loginform")
		br.form["log"] = email
		br.form["pwd"] = "123456"
		br.submit()
		respuestaWP = br.response().geturl()
		html =  br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		divError = soup.findAll("div", {"id": "login_error"})
		div = remove_tags(str(divError))
		if "incorrect" in div:
			print "|--[INFO][WordPress][CHECK][>] The account exist..."
			if state == 1:
				print colores.blue + "|--[INFO][WordPress][CHECK][>] it's possible to hack it !!!" + colores.normal
		if "Invalid" in div:
			print "|--[INFO][WordPress][CHECK][>] Account doesn't exist..."
	except:
		print colores.alert + "|--[WARNING][LinkedIn][>] Error..." + colores.normal

def check_badoo(email, state):
	try:
		r = br.open('https://badoo.com/es/signin/')
		br.select_form(nr=0)
		br.form["email"] = email
		br.form["password"] = "123456123456"
		br.submit()
		respuestaURL = br.response().geturl()
		html =  br.response().read()
		if "Usuario" in html and state == 1:
			print colores.blue + "|--[INFO][Badoo][CHECK][>] it's possible to hack it !!!" + colores.normal
		else:
			print "|--[INFO][Badoo][CHECK][>] Account doesn't exists..."
	except:
		print colores.alert + "|--[WARNING][Badoo][>] Error..." + colores.normal

def check_amazon(email, state):
	r = br.open('https://www.amazon.es/ap/signin?_encoding=UTF8&openid.assoc_handle=esflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_signin')
	br.select_form("signIn")
	br.form["email"] = email
	br.form["password"] = "123456123456"
	br.submit()
	respuestaURL = br.response().geturl()
	html =  br.response().read()
	soup = BeautifulSoup(html, "html.parser")
	for div in soup.findAll("li"):
		#div = remove_tags(str(div))
		print div
	if "correcta" in div:
		print "|--[INFO][Amazon.es][CHECK][>] The account exist..."
		if state == 1:
			print colores.blue + "|--[INFO][Amazon.es][CHECK][>] it's possible to hack it !!!" + colores.normal
	if "Indica" in div:
		print "|--[INFO][Amazon.es][CHECK][>] Account doesn't exists..."
	#except:
	#	print colores.alert + "|--[WARNING][Amazon.es][>] Error..." + colores.normal

def check_tumblr(email, state):
	r = br.open('https://www.tumblr.com/login')
	print r.read()
	br.select_form(nr=0)
	br.form["determine_email"] = email
	#br.form["pwd"] = "123456"
	br.submit()
	respuestaURL = br.response().geturl()
	print respuestaURL
	if "yahoo" in respuestaURL and state == 1:
		print colores.blue + "|--[INFO][Tumblr][CHECK][>] it's possible to hack it !!!" + colores.normal
	else:
		print "|--[INFO][Tumblr][CHECK][>] Account doesn't exist..."

def check_hesidohackeado(email):
	url = "https://hesidohackeado.com/api?q=" + email
	html = br.open(url).read()
	data = json.loads(html)
	print colores.green + "|--[INFO][HESIDOHACKEADO][>] " + colores.normal + "Results: " + str(data["results"])
	for i in range(0,data["results"]):
		print colores.green + "|--[INFO][HESIDOHACKEADO][URL][>] " + colores.normal +  str(data["data"][i]["source_url"])
		print colores.green + "|--[INFO][HESIDOHACKEADO][DETAILS][>] " + colores.normal + str(data["data"][i]["details"])

def check_pastebin(email):
	url = "http://pastebin.com/search?q=" + email.replace(" ", "+")
	print "|--[INFO][PASTEBIN][SEARCH][>] " + url + "..."
	html = br.open(url).read()
	soup = BeautifulSoup(html, "html.parser")
	for div in soup.findAll("div", {"class", "gsc-thumbnail-inside"}):
		print "|--[INFO][PASTEBIN][URL][>]" + str(div)

def banner():
	print """
███████╗ ██████╗       ██████╗ ██╗██████╗ ██████╗ ███████╗██████╗    ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗      ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝██╔══██╗   ██╔══██╗╚██╗ ██╔╝
█████╗  ██║   ██║█████╗██████╔╝██║██████╔╝██████╔╝█████╗  ██████╔╝   ██████╔╝ ╚████╔╝ 
██╔══╝  ██║   ██║╚════╝██╔══██╗██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗   ██╔═══╝   ╚██╔╝  
███████╗╚██████╔╝      ██║  ██║██║██║     ██║     ███████╗██║  ██║██╗██║        ██║   
╚══════╝ ╚═════╝       ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
      Author: Jorge Websec | Twitter: @JorgeWebsec | jorge.coronado@quantika14.com
-------------------------------------------------------------------------------------
[!]What can I know with your email?
    - Only 1 email or emails list
    - Verify emails
    - Verify LinkedIn, WordPress, Badoo, Amazon, Tumblr
    - Hesidohackeado.com
    - Pastebin
-------------------------------------------------------------------------------------
Date latest version: 09/01/2017 | Version: 1.0
-------------------------------------------------------------------------------------
"""

def menu():
	print ""
	print "------------------------------------------------------------------------"
	print "--- 1. Emails list (default: emails.txt)                             ---"
	print "--- 2. Only one target                                               ---"
	print "------------------------------------------------------------------------"
	print ""
	x = int(raw_input("Select 1/2: "))
	if type(x) != int:
		print "[Warning][Menu][>] Error..."
		menu()
	else:
		return x

def attack(email):
	email = email.replace("\n", "")
	url = "http://www.verifyemailaddress.org/es/"
	html = br.open(url)
	br.select_form(nr=0)
	br.form['email'] = email
	br.submit()
	resp = br.response().read()
	soup = BeautifulSoup(resp, "html.parser")
	state = 0
	for li in soup.find_all('li', {'class':"success valid"}):
		verif = remove_tags(str(li))
		print verif
		if len(verif)>5:
			print "[INFO][TARGET][>] " + email
			print "|--[INFO][EMAIL][>] Email validated..."
		else:
			state = 1
			print "[INFO][TARGET][>] " + email
			print "|--[INFO][EMAIL][>] It's not created..."

	check_linkedin(email, state)
	check_wordpress(email, state)
	check_badoo(email, state)
	#check_amazon(email,state)
	#check_tumblr(email, state)
	check_hesidohackeado(email)
	check_pastebin(email)

#Hilo Principal
def main():
	global emails_list
	banner()
	m = menu()
	if m == 1:
		print "[INFO][Emails list][>] By default 'emails.txt'..."
		print "[INFO][Emails list][>] If you want by default, press ENTER."
		file = open(emails_list, 'r')
		for email in file.readlines():
			attack(email)
	if m == 2:
		email = str(raw_input("Email: "))
		attack(email)

if __name__ == "__main__":
	main()
