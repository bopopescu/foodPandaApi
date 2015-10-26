from bs4 import BeautifulSoup
import socket
import requests
from re import sub
from re import search
# from locality import find_foodpanda_valid_locality,find_locality


def find_all_restaurants(loca):
	restaurants = []
	searchurl = "https://www.foodpanda.in/location-suggestions?cityId=11&area=%s" % (loca[1])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	data = BeautifulSoup(str(soup.find_all("div",{'class':'vendor__title'})))
	for link in data.find_all("a"):
		uniqueId = search('/restaurant/(.+?)">', str(link)).group(1)
		restaurantName = link.text
		restaurants.append((str(uniqueId),str(restaurantName)))
	print restaurants
	f = open("outputRestaurants.txt","w")
	f.write(str(restaurants))
	f.close()
	return restaurants

def restaurant_info(restaurantsData,localities):
	searchurl = "https://www.foodpanda.in/restaurant/%s" % (restaurantsData[0])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	restaurantsData += (str(sub(r"[^\x00-\x7F]+","",(soup.find('address').text))),)
	restaurantsData += (float((soup.find('i',{'class':'stars'}))['content']),)
	details = sub("(?m)^\s+","",str(soup.find('ul',{'class':'cart__empty__elements'}).text)).split('\n')
	deliveryFee = None
	deliveryTime = None
	paymentOption = None
	deliveryMinAmount = None
	Voucher = False
	pickupTime = None
	for index,item in enumerate(details):
		if(item == 'Delivery time:'):
			deliveryTime = details[index+1]
		elif(item == 'Online payment available'):
			paymentOption = True
		elif(item == 'Delivery fee'):
			deliveryFee = float(sub(",","",sub("Rs.","",details[index+1])))
		elif(item == 'Delivery min.:'):			
			deliveryMinAmount = float(sub(",","",sub("Rs.","",details[index+1])))
		elif(item == 'Accepts Vouchers'):
			Voucher = True
	if(soup.find("dt",{"class":"vendor-pickup-time"}) != None ):
		soup2 = BeautifulSoup(str(soup.find("dt",{"class":"vendor-pickup-time"}).findNext("dd")))
		data = soup2.find("dd").text
		pickupTime = (sub("(?m)^\s+","",str(data)).split("\n")).pop(0)
	restaurantsData += (deliveryFee,deliveryTime,pickupTime,deliveryMinAmount,paymentOption,Voucher,searchurl,localities[0],)
	print restaurantsData
	f = open("outputRestaurantsComplete.txt","w")
	f.write(str(restaurantsData))
	f.close()
	return restaurantsData

	#for index,item in enumerate(restaurantsData):
	#	soup.
def food_info(restaurantsData,count):
	foodData = []
	print restaurantsData
	print count
	searchurl = "https://www.foodpanda.in/restaurant/%s" % (restaurantsData[0])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	string =''
	for data in soup.find_all('div',{'class':'menu-item__content-wrapper'}):
		soup2 = BeautifulSoup(str(data))
		dish_name = soup2.find('div', {'class': 'menu-item__title'}).text
		for val in soup2.find_all('article', {'class': 'menu-item__variation'}):
			string += (sub("(?m)^\s+","",dish_name))
			string += (sub("(?m)^\s+","",val.text))
	string = string.strip().split('\n')
	for index,item in enumerate(string):
		if item == u'\xa0':
			string.pop(index)
		# print string
	foodtuple = ()
	itemCount = 0 
	foodtuple += (count,restaurantsData[0],)	
	for index,item in enumerate(string):
		if item == 'Add':
			itemCount = 0
			foodData.append(foodtuple+ (searchurl,))
			count += 1
			foodtuple = ()
			foodtuple += (count,restaurantsData[0],)			 
		else:
			item = item.replace(unichr(160),'')
			if "Rs." in str((sub(r"[^\x00-\x7F]+","",item))) and itemCount%2 == 1:
				item = sub("Rs.","",str((sub(r"[^\x00-\x7F]+","",item))))
				item = sub(",","",str(item))
				foodtuple += ('None',float(item),)
				itemCount += 1
			elif "Rs." in str((sub(r"[^\x00-\x7F]+","",item))):
				item = sub("Rs.","",str((sub(r"[^\x00-\x7F]+","",item))))
				item = sub(",","",str(item))
				foodtuple += (float(item),)
			else:
				foodtuple += (str((sub(r"[^\x00-\x7F]+","",item))),)
				itemCount += 1
	return foodData

		# print (sub("(?m)^\s+","",data.text))
	


# restaurantsData = find_all_restaurants(localities)
# restaurant_info(restaurantsData)
# foodDB = food_info(restaurantsData)