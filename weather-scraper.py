#Plan: make a bot that scrapes accuweather for all the daily high and low temps it has.

import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.accuweather.com/en/us/new-york/10007/daily-weather-forecast/349727" 
page_selector = "?page={}" #this thing gets a page number plugged into it and then is appended to the url to give the correct page
page_range = range(0, 7)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"} #very nice this fixed the 403 but i have no idea what it does atm

def scrape_pages(): #scrapes all the pages, returns a list of soups
	soup_list = []
	for page_number in page_range:
		url = base_url + page_selector.format(page_number)
		
		page = requests.get(url, headers=headers) #the headers thing is to prevent a 403 forbidden error
		soup = BeautifulSoup(page.text, "html.parser")
		
		soup_list.append(soup)
		
	return soup_list #I mean, I know stopping and creating this list of soups is unnecessary (I could go straight to parsing without saving soup_list), but I think it'd somehow be messy to do that. Also, maybe it makes debugging easier?
	
def parse_soup_list(soup_list):
	day_list = [] #this will be the output
	for soup in soup_list:
		for day_div in soup.find_all("div", class_="daily-wrapper"): #why is that underscore there in "class_"? is it "class" is a special term that you don't want to mess with? Actually yeah that probably makes sense   #also that thing about looking for a div doesn't need to be there but I think it helps comprehension
			day = {}
			
			#could probably make this next step more compact by making a dict matching each value to some xml locator or something but that sounds like a waste of time rn
			day["date"] = day_div.find(class_="sub").get_text()
			day["high"] = day_div.find(class_="high").get_text()
			day["low"] = day_div.find(class_="low").get_text()
			day["precip"] = day_div.find(class_="precip").get_text()
			
			#now to clean up the values stored in the dict so that they're all only numbers
			for key in day:
				day[key] = re.findall("[0-9]+", day[key])
			
			#wait now I wanna add in the day of the week
			day["weekday"] = day_div.find(class_="dow").get_text()
			
			day_list.append(day)
			
	return day_list
	
def print_day_list(day_list):
	for day in day_list:
		print("{} {}/{} temp {}-{} precip {}%".format(day["weekday"], day["date"][0], day["date"][1], day["low"][0], day["high"][0], day["precip"][0])) #hur dur
		if day["weekday"] == "Sat":
			print("-")
		
if __name__ == "__main__": #is this check necessary? probably not
	print("scraping... url: {}".format(base_url))
	soup_list = scrape_pages()
	print(soup_list)
	print("parsing...")
	day_list = parse_soup_list(soup_list)
	print(day_list)
	print("printing...")
	print_day_list(day_list)
