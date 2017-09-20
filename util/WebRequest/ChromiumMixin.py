#!/usr/bin/python3

import time
import os.path
import random
import socket
import urllib.parse
import http.cookiejar
import bs4
import ChromeController


class WebGetCrMixin(object):
	# creds is a list of 3-tuples that gets inserted into the password manager.
	# it is structured [(top_level_url1, username1, password1), (top_level_url2, username2, password2)]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._cr = None
		self._cr_port = 9222
		self._cr_binary = "google-chrome"
		# self._initChromium()



	def _initChromium(self):
		for _ in range(25):
			try:
				self._cr = ChromeController.ChromeRemoteDebugInterface(
						self._cr_binary,
						dbg_port = self._cr_port,
					)
				return
			except (ChromeController.ChromeConnectFailure,
					ChromeController.ChromeStartupException):
				self._cr_port += 1

	def _syncIntoChromium(self):
		# Headers are a list of 2-tuples. We need a dict
		hdict = dict(self.browserHeaders)
		self._cr.update_headers(hdict)
		for cookie in self.cj:
			self._cr.set_cookie(cookie)

	def _syncOutOfChromium(self):
		for cookie in self._cr.get_cookies():
			self.cj.set_cookie(cookie)

	def getItemChromium(self, itemUrl):
		self.log.info("Fetching page for URL: '%s' with Chromium" % itemUrl)

		if not self._cr:
			self._initChromium()

		self._syncIntoChromium()

		response = self._cr.blocking_navigate_and_get_source(itemUrl, timeout=10)

		raw_url = self._cr.get_current_url()
		fileN = urllib.parse.unquote(urllib.parse.urlparse(raw_url)[2].split("/")[-1])
		fileN = bs4.UnicodeDammit(fileN).unicode_markup

		self._syncOutOfChromium()

		# Probably a bad assumption
		if response['binary']:
			mType = "application/x-binary"
		else:
			mType = "text/html"

		# So, self._cr.page_source appears to be the *compressed* page source as-rendered. Because reasons.
		content = response['content']
		return content, fileN, mType

	def getHeadTitleChromium(self, url, referrer=None):
		self.log.info("Getting HEAD with Chromium")
		if not referrer:
			referrer = url

		if not self._cr:
			self._initChromium()
		self._syncIntoChromium()

		self._cr.blocking_navigate(referrer)
		time.sleep(random.uniform(2, 6))
		self._cr.blocking_navigate(url)

		title, cur_url = self._cr.get_page_url_title()

		self._syncOutOfChromium()

		ret = {
			'url': cur_url,
			'title': title,
		}
		return ret

	def getHeadChromium(self, url, referrer=None):
		self.log.info("Getting HEAD with Chromium")
		if not referrer:
			referrer = url

		if not self._cr:
			self._initChromium()
		self._syncIntoChromium()

		self._cr.blocking_navigate(referrer)
		time.sleep(random.uniform(2, 6))
		self._cr.blocking_navigate(url)

		dummy_title, cur_url = self._cr.get_page_url_title()

		self._syncOutOfChromium()

		return cur_url

	def close_chromium(self):
		if self._cr != None:
			self._cr.close()
			self._cr = None

	def __del__(self):
		self.close_chromium()

	# def stepThroughCloudFlare_cr(self, url, titleContains='', titleNotContains=''):
	# 	'''
	# 	Use Selenium+Chromium to access a resource behind cloudflare protection.

	# 	Params:
	# 		``url`` - The URL to access that is protected by cloudflare
	# 		``titleContains`` - A string that is in the title of the protected page, and NOT the
	# 			cloudflare intermediate page. The presence of this string in the page title
	# 			is used to determine whether the cloudflare protection has been successfully
	# 			penetrated.

	# 	The current WebGetRobust headers are installed into the selenium browser, which
	# 	is then used to access the protected resource.

	# 	Once the protected page has properly loaded, the cloudflare access cookie is
	# 	then extracted from the selenium browser, and installed back into the WebGetRobust
	# 	instance, so it can continue to use the cloudflare auth in normal requests.

	# 	'''

	# 	if (not titleContains) and (not titleNotContains):
	# 		raise ValueError("You must pass either a string the title should contain, or a string the title shouldn't contain!")

	# 	if titleContains and titleNotContains:
	# 		raise ValueError("You can only pass a single conditional statement!")

	# 	self.log.info("Attempting to access page through cloudflare browser verification.")

	# 	dcap = dict(DesiredCapabilities.Chromium)
	# 	wgSettings = dict(self.browserHeaders)

	# 	# Install the headers from the WebGet class into Chromium
	# 	dcap["Chromium.page.settings.userAgent"] = wgSettings.pop('User-Agent')
	# 	for headerName in wgSettings:
	# 		dcap['Chromium.page.customHeaders.{header}'.format(header=headerName)] = wgSettings[headerName]

	# 	driver = selenium.webdriver.Chromium(desired_capabilities=dcap)
	# 	driver.set_window_size(1024, 768)

	# 	driver.get(url)

	# 	if titleContains:
	# 		condition = EC.title_contains(titleContains)
	# 	elif titleNotContains:
	# 		condition = title_not_contains(titleNotContains)
	# 	else:
	# 		raise ValueError("Wat?")

	# 	try:
	# 		WebDriverWait(driver, 20).until(condition)
	# 		success = True
	# 		self.log.info("Successfully accessed main page!")
	# 	except TimeoutException:
	# 		self.log.error("Could not pass through cloudflare blocking!")
	# 		success = False
	# 	# Add cookies to cookiejar

	# 	for cookie in driver.get_cookies():
	# 		self.addSeleniumCookie(cookie)
	# 		#print cookie[u"value"]

	# 	self.__syncCookiesFromFile()

	# 	return success
