from bs4 import BeautifulSoup
from urllib import request as req

small_size  = BeautifulSoup(req.urlopen('http://dogtime.com/dog-breeds/characteristics/small').read(), 'html.parser')
medium_size = BeautifulSoup(req.urlopen('http://dogtime.com/dog-breeds/characteristics/medium').read(), 'html.parser')
large_size  = BeautifulSoup(req.urlopen('http://dogtime.com/dog-breeds/characteristics/size').read(), 'html.parser')

small_list, medium_list, large_list = [], [], []

for breed in small_size.findAll('span', {'class' : 'post-title'}):
    small_list.append(breed.getText())

for breed in medium_size.findAll('span', {'class' : 'post-title'}):
    medium_list.append(breed.getText())

for breed in large_size.findAll('span', {'class' : 'post-title'}):
    large_list.append(breed.getText())

print('Small Breeds:')
print(small_list)

print('Medium Breeds:')
print(medium_list)

print('Large Breeds:')
print(large_list)