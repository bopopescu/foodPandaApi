from foodpanda_locality import insertManyLocalities, insertOneLocality, findLocalitiesByCityId
from foodpanda_city import insertManyCities
from foodpanda_restaurants import insertManyRestaurants, insertOneRestaurant ,findRestaurantsByLocalityId
from foodpanda_menu import insertManyDishes
from crawlers.restaurant import find_all_restaurants,restaurant_info,food_info

def main():
	lengthOfFoodDB = 0
	foodPandaLoca = findLocalitiesByCityId('11')
	for item in foodPandaLoca:
	# for item in foodPandaLoca:
	# 	print item
	# 	insertOneLocality(item[0], item[1], item[2], item[3])
	# # insertManyCities(city_List())
	# = find_foodpanda_valid_locality('Bangalore',loca)
	# insertManyLocalities(foodPandaLoca)
		restaurantDB = findRestaurantsByLocalityId(item[0])
		for restaurant in restaurantDB:
			foodDB = food_info(restaurant,lengthOfFoodDB)
			lengthOfFoodDB += len(foodDB)
			insertManyDishes(foodDB)
	# insertManyDishes(food_info(restaurantDB))

if __name__ == '__main__':
	main()