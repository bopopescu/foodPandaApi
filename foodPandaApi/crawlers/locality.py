from bs4 import BeautifulSoup
import socket
import requests
from re import sub,search
from city import city_List


cityList = city_List()
def find_locality(cityName):
	searchurl = "http://www.commonfloor.com/localities/index/city/%s" % (cityName)
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	localities=[]
	data = soup.find('tbody')
	data= str(sub("(?m)^\s+", "", str(data.text)))
	data = data.split('\n')
	for item in data:
		if item.isalpha():
			localities.append(item)
	print localities
	return localities
def find_foodpanda_valid_locality(cityName,localities):
	foodpanda_locality = []
	tempraroy_list1 = []
	tempraroy_list2 = []
	for loca in localities:
		searchurl = "https://www.foodpanda.in/location-suggestions?cityId=11&area=%s" % (loca)
		f = requests.get(searchurl)
		html = f.text
		soup = BeautifulSoup(html)
		if(soup.find('h1',{'class':'h2'})):
			heading = sub(":","",soup.find('h1',{'class':'h2'}).text)
			heading = heading.strip()
			if heading=="Suggestions":		
				
				tempraroy_list1[:] = []
				for data in soup.find_all('a',{'class':'list-group-item'}):
					tempraroy_list1.append(search('area_id=(.+?)">', str(data)).group(1))
				
				# #print tempraroy_list
				# for item in tempraroy_list:
				# 	foodpanda_locality.append((item,))
				#print foodpanda_locality
				
				tempraroy_list2[:] = []
				for data in soup.find_all('div',{'class':'content-block location-suggestions'}):
					tempraroy_list2= sub("(?m)^\s+","",data.text).split('\n')
				tempraroy_list2.pop(0) 												# poping "Suggestion" string
				tempraroy_list2.pop(len(tempraroy_list2)-1)				 							# poping whitespace
				#print tempraroy_list
				
				for cityTuple in cityList:
					if(cityTuple[1]==cityName):
						for locality,area_id in zip(tempraroy_list2,tempraroy_list1):
							searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (area_id) 
							foodpanda_locality.append((area_id,str((locality).replace(unichr(8226),'')),str(cityTuple[0]),searchurl,))
				#print foodpanda_locality
				# break
		else:
			data = soup.find('meta',{'property':'og:url'})
			area_id = search('area_id=(.+?)">',str(data))
			for cityTuple in cityList:
				if(cityTuple[1]==cityName):
					searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (area_id) 
					foodpanda_locality.append((area_id,str(loca),str(cityTuple[0]),searchurl,))
	# for index,item in enumerate(foodpanda_locality):
	# 	if len(item) != 4:
	# 		foodpanda_locality.pop(index)
	#print foodpanda_locality
	
	# To remove repetitive elements
	# new_list = []
	# new_list.append(foodpanda_locality[0])
	# for item in foodpanda_locality:
	# 	print 'item in first loop : ',item
	# 	for item2 in new_list:
	# 		print 'item in second loop : ',item2
	# 		if (item[0] != item2[0]):
	# 			new_list.append(item) 
	# return new_list
	return foodpanda_locality


# loca = find_locality('Bangalore')
# find_foodpanda_valid_locality('Bangalore',loca)
