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

# Website for this cat does not exist
CatPage = "https://thiscatdoesnotexist.com/"
# Use requests.get to pull the image from the page
CatResult = requests.get(CatPage, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})

#For now, just an array of cat sounds, because I'm lazy
# To do: something better
Meow_Array=['meow', 'mew', 'MEOW', 'mmmm', 'mrrr', 'mauu', 'mrow', 'prrrr', '*HISS*', 'i gotta have my lasaga']
#Limited to the amount in the array
meow_num=randint(0,9)
#Now the message is chosen at random
msg=Meow_Array[meow_num]


# real life cat waifus... err, cats
img = (Image.open(BytesIO(CatResult.content)))
# Not necessary to show the image but useful for testing
#img.show()
# Save the image to the local folder for loading, not necessarily required
img.save('cat.jpg')
# The token to post for facebook. This will be blank on github
token=""

# Define the standard post to facebook function via the facebook graph api
def postToFacebook(token, message=msg):
	graph = facebook.GraphAPI(token)
	post_id = graph.put_photo(image = open('cat.jpg', 'rb'), message = message)["post_id"]
	print(f"Successfully posted {post_id} to facebook", file=open("cat_bot_log.log", "a"))

# Finally, we actually post to facebook!
postToFacebook(token)
# Pull the current date and print it to the log, for testing and maintenance
nowdate= datetime.datetime.now()
print(nowdate, file=open("cat_bot_log.log", "a"))

