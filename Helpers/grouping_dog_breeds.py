'''
This script is used to crawl dogs.petbreeds.com to search for breeds group by some characteristics as size, temperaments, etc;
'''

import json
from urllib.request import Request, urlopen

BREED_GROUPS = {
	'SIZE' : {},
	'TEMPERAMENT' : {},
	'TRAINABILITY' : {},
	'KIDS' : {},
	'GROOMING' : {}
}

def map_breed(dict, label):
	for k, v in dict.items():
		page = 0
		BREED_GROUPS[label][k] = set()
		
		while 0==0:
			req = Request(v.format(page), headers={'User-Agent': 'Mozilla/5.0'})
			data = json.loads(urlopen(req).read().decode('utf-8'))

			target = data['data']['data']
			
			# Results ended
			if len(target) == 0:
				break

			for i in range(len(target)):
				BREED_GROUPS[label][k].add(target[i][1].upper())
			
			page += 1

def group_breeds_helper():
	# API URL's (Extracted directly from website)

	# BY SIZE -------------------------
	URL_TOY = 'http://dogs.petbreeds.com/ajax_search?_len=10000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=collection_breed_size&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=1&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_SMALL = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=collection_breed_size&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=2&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_MEDIUM = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=collection_breed_size&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=3&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_LARGE = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=collection_breed_size&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=4&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_GIANT = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=collection_breed_size&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=5&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'

	URLS_BY_SIZE = {'toy' : URL_TOY, 'small' : URL_SMALL, 'medium' : URL_MEDIUM, 'large' : URL_LARGE, 'giant' : URL_GIANT} 

	# BY TEMPERAMENT -------------------------
	URL_FRIENDLY = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=temper&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=14&_fil%5B0%5D%5Bvalue%5D%5B%5D=17&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_AGRESSIVE = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=temper&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=1&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'

	URLS_BY_TEMPERAMENT = {'friendly' : URL_FRIENDLY, 'agressive' : URL_AGRESSIVE} 

	# BY TRAINABILITY -------------------------
	URL_EASY = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=trainability&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=1&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_MEDIUM = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=trainability&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=2&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_HARD = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=trainability&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=3&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'

	URLS_BY_TRAINABILITY = {'easy' : URL_FRIENDLY, 'medium' : URL_AGRESSIVE, 'hard' : URL_HARD} 

	# GOOD WITH KIDS --------------------------
	URL_GOOD_WITH_KIDS = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=goodchild&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=1&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_NOT_GOOD_WITH_KIDS = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=goodchild&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=2&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'

	URLS_BY_KIDS = {'good' : URL_GOOD_WITH_KIDS, 'not_good' : URL_NOT_GOOD_WITH_KIDS} 

	# BY GROOMING ------------------------------
	URL_LOW_MAINTENECE = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=grooming_needs&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=1&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_MEDIUM_MAINTENENCE = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=grooming_needs&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=2&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'
	URL_HIGH_MAINTENENCE = 'http://dogs.petbreeds.com/ajax_search?_len=1000&page={0}&app_id=465&_sortfld=_GC_srp_rank&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=grooming_needs&_fil%5B0%5D%5Boperator%5D=%3D&_fil%5B0%5D%5Bvalue%5D%5B%5D=3&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=dogbreed&head%5B%5D=breed_type&head%5B%5D=_urr_avg_rating&head%5B%5D=_GC_srp_rank&head%5B%5D=temper&head%5B%5D=life_avg&head%5B%5D=weight&head%5B%5D=maxheight&head%5B%5D=collection_goodchildren&head%5B%5D=popularity_2015&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=popularity_proper_sort&head%5B%5D=_avg_rating&head%5B%5D=_num_reviews'

	URLS_BY_GROOMING = {'low' : URL_LOW_MAINTENECE, 'medium' : URL_MEDIUM_MAINTENENCE, 'high' : URL_HIGH_MAINTENENCE} 

	# Processing ---------------
	print('Processing sizes...')
	map_breed(URLS_BY_SIZE, 'SIZE')
	print('Processing temperaments...')
	map_breed(URLS_BY_TEMPERAMENT, 'TEMPERAMENT')
	print('Processing trainability...')
	map_breed(URLS_BY_TRAINABILITY, 'TRAINABILITY')
	print('Processing kids...')
	map_breed(URLS_BY_KIDS, 'KIDS')
	print('Processing grooming...')
	map_breed(URLS_BY_GROOMING, 'GROOMING')

	# Writing
	print('Done! Writing...')
	f = open('BREED_GROUP.py', 'w', encoding='utf-8')
	f.write('BREED_GROUPS = ' + str(BREED_GROUPS))
	print('Writing complete!')

group_breeds_helper()