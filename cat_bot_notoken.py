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
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Website for this cat does not exist
CatPage = "https://thiscatdoesnotexist.com/"
# Use requests.get to pull the image from the page
CatResult = requests.get(CatPage, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})

#doing: something better
inp = pd.read_csv('/home/pi/Desktop/Python/Cat_DNE_Bot/nounlist.txt')
inp2 = pd.read_csv('/home/pi/Desktop/Python/Cat_DNE_Bot/sounds.txt')
inp3 = pd.read_csv('/home/pi/Desktop/Python/Cat_DNE_Bot/verbs.txt')

#this outputs the top three lines, but not necessary for production
#inp.head(3)

#new message
cat_name = inp["NOUNS"].iloc[randint(0,6855)].capitalize()

verb_rand1 = randint(0,1)
verb_rand2 = randint(0,1)

if verb_rand1 == 0:
    likes = "the " + inp["NOUNS"].iloc[randint(0,6855)]
else:
    likes = "to" + inp3["VERBS"].iloc[randint(0,183)] + " the " + inp["NOUNS"].iloc[randint(0,6855)]

if verb_rand2 == 0:
    dislikes = "the " + inp["NOUNS"].iloc[randint(0,6855)]
else:
    dislikes = "to" + inp3["VERBS"].iloc[randint(0,183)] + " the " + inp["NOUNS"].iloc[randint(0,6855)]

sound_rand = randint(0,100)
if (sound_rand > 75):
    sound = inp2["SOUNDS"].iloc[randint(0,465)] + " " + inp2["SOUNDS"].iloc[randint(0,465)]
else:
    sound = inp2["SOUNDS"].iloc[randint(0,465)]
    
msg = "Name: " + cat_name + "\n\n" + "This cat likes: " + likes + "\n\n" + "This cat dislikes: " + dislikes + "\n\n" + "This cat makes this sound: " + sound

print(msg)
# real life cat waifus... err, cats
img = (Image.open(BytesIO(CatResult.content)))
# Not necessary to show the image but useful for testing
#img.show()
# Save the image to the local folder for loading, not necessarily required
img.save('cat.jpg')
# The token to post for facebook. This will be blank on github
token=""	#removed token for github

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
