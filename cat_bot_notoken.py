# import requests for html parsing
import requests
# import randint for random number generation
from random import randint
# import Image for image processing
from PIL import Image
# import BytesIO for image pull
from io import BytesIO
# import codecs for decoding/encoding to handle japanese text
import codecs
# import facebook to actually post the post
import facebook
# import logging for future use
import logging
# testing markov chains
import random as randm
import numpy as nmpy
import datetime
# Just leftovers from WaifuBot
# I may use the text parsing for adding text to the 

# TWDNE website is very intuitive. Every image is stored as integer.jpg
# where integer is between 1 and 100,000
#Waifu_Url = "https://www.thiswaifudoesnotexist.net/example-"+str(waifu_number)+".jpg"
#print(Waifu_Url)

# Use the text_number for pulling text snippet
#Text_Url = "https://www.thiswaifudoesnotexist.net/snippet-"+str(text_number)+".txt"
#print(Text_Url)

# Here we use requests to get the text snippet
#data = requests.get(Text_Url)
# Very important! Format the content of data as a string, with utf-8 encoding
# This ensures that the Japanese text looks good!
#data2 = str(data.content, 'utf-8', errors='replace')

# Addendum for ellipses
# Next, we split the text into sentences, and store in a list
#data3 = str(data2).replace('...', 'ELLIPSES').split('.')
# Print for spacing

#print(data3)

# New idea
# Take total length of the list
# Generate a random number of sentences, like 3-5
# create upper bound and lower bound so there's no overflow
# Max length - numsen for upper bound
# No lower bound?
# Then we just start off from there

#Number_of_Sentences = randint(4,6)
#print("Number_of_Sentences")
#print(Number_of_Sentences)

# upper text bound is the total length of the list data3 (number of total sentences)
#upper_text_bound = (len(data3) - Number_of_Sentences - 1)

# These were for testing only
#upper_text_bound = 3
#print("upper_text_bound")
#print(upper_text_bound)

# Lower bound is a random number between 1 and the upper text bound
# So if we want three sentences, it will start between the first the third to last
#Lower_Bound = randint( 1, upper_text_bound)
#print("Lower_Bound")
#print(Lower_Bound)

# True upper bound is the actual upper bound of the text we're pulling
# So Lower bound is our start and true upper bound is the end
#True_Upper_Bound = Lower_Bound + Number_of_Sentences
#print("True_Upper_Bound")
#print(True_Upper_Bound)


# # Here, we create a blank string object known as data4
# data4 = ""

# # We have to create a function to easily append the sentences to the string

# print('data 3 as a string')


# Now, each sentence is pulled from the data3 variable, given punctuation,
# and appended to the data4 string
# for i in range(Lower_Bound,True_Upper_Bound):
# 	data4 = data4+str(data3[i]+'.')

# # To fix the ellipses
# data4 = str(data4).replace( 'ELLIPSES' , '...' )
# data5 = data4.encode('utf-8')
# #print(data4)
# #print(data3.split('.'))

# For future use: this cat does not exist
CatPage = "https://thiscatdoesnotexist.com/"
CatResult = requests.get(CatPage, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})

#For now, just an array of cat sounds
Meow_Array=['meow', 'mew', 'MEOW', 'mmmm', 'mrrr', 'mauu', 'mrow', 'prrrr', '*HISS*', 'i gotta have my lasaga']
#Limited to the amount in the array
meow_num=randint(0,9)
#Now the message is chosen at random
msg=Meow_Array[meow_num]


# real life cat waifus
img = (Image.open(BytesIO(CatResult.content)))
#img.show()
img.save('cat.jpg')
token=""

def postToFacebook(token, message=msg):
	graph = facebook.GraphAPI(token)
	post_id = graph.put_photo(image = open('cat.jpg', 'rb'), message = message)["post_id"]
	print(f"Successfully posted {post_id} to facebook")

postToFacebook(token)
#print(data5)
nowdate= datetime.datetime.now()
print(nowdate, file=open("cat_bot_log.log", "a"))

