import streamlit as st
import tweepy 
import re 
import snscrape.modules.twitter as sntwitter
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
import xlwt 
from xlwt import Workbook
import csv

st.title("Products")
st.subheader("Newest tech: ")

# Set up your Twitter API credentials
consumer_key = "TyAvYBzGjRB3rjDvNLL05qnTb"
consumer_secret = "QCpB0HsJ4FbrmBKdHXYEbbOwQEUXmfa2fEnpJvP8tZW3wTJq3k"
access_token = "1678938637013057537-22b4nk9BMOKTELoyz2MolKEI9h9bWb"
access_token_secret = "BE97lESzGGFR3USDOPfldxfTbhlCQzBdN6j5sVKKDoPc0"
#bearer_toker = "AAAAAAAAAAAAAAAAAAAAANb7ogEAAAAAQZTMSQ185CS1cZdAfQCYS0Mdkqg%3DyOLXXHUUcwNmu10ftkY0gsgZegBFBbWM6nlEmtDp9Qc8w6GpMl"
#Client ID = "a081SXIxNGZJeXFjbVl2SnVuZ186MTpjaQ"
#Client Secret = "I0i3VI8zR3WEY1xMe7592UPeBe9VWVh8HoFVelXcG3V1lDBGHA"

#client = tweepy.Client(bearer_token = "AAAAAAAAAAAAAAAAAAAAANb7ogEAAAAAQZTMSQ185CS1cZdAfQCYS0Mdkqg%3DyOLXXHUUcwNmu10ftkY0gsgZegBFBbWM6nlEmtDp9Qc8w6GpMl")

##client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)


# Authenticate with Twitter
##auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
##auth.set_access_token(access_token, access_token_secret)
##api = tweepy.API(auth)

# Set the number of tweets you want to retrieve
##tweet_count = 5

# Define a list of keywords to search for fashionable products
##keywords = ["fashion", "style", "clothing", "accessories"]

# Set the minimum number of likes required
##min_likes = 100000

# Fetch the tweets for each keyword and filter by likes
##for keyword in keywords:
##    st.header(f"Tweets for keyword: {keyword}")
    
    #tweets = tweepy.Cursor(api.search, q=keyword, count=tweet_count, result_type="popular", tweet_mode="extended").items(tweet_count)
    #tweets = api.search_tweets(q=keyword, count=tweet_count, result_type="popular", tweet_mode="extended")
    #tweets = tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode="extended").items(tweet_count)

    #filtered_tweets = [tweet for tweet in tweets if tweet.favorite_count >= min_likes]


 ##   query = f"{keyword} -is:retweet"
 ##   tweets = client.search_recent_tweets(query=query, tweet_fields=['public_metrics', 'created_at'], max_results=tweet_count)
    
 ##   sorted_tweets = sorted(tweets.data, key=lambda t: t.public_metrics.like_count, reverse=True)
  ##  filtered_tweets = [tweet for tweet in sorted_tweets if tweet.public_metrics.like_count >= min_likes]

    
  ##  for tweet in filtered_tweets:

   ##     st.subheader(f"Tweet: {tweet.full_text}")
   ##     st.write(f"Likes: {tweet.favorite_count}")

        # Refine the regular expression pattern
   ##     product_names = re.findall(r"(?i)\b(?:[A-Z][a-zA-Z&'-]+\s?)+\b", tweet.text)
   ##     st.write(f"Product Names: {product_names}")

   ##     st.write("-" * 30)

#(from:elonmusk) until:2020-01-01 since:2010-01-01
query = "python"
tweets = []
limit = 10


#for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    # print(vars(tweet))
    # break
   #if len(tweets) == limit:
     #   break
   # else:
   #     tweets.append([tweet.date, tweet.username, tweet.content])
   #     st.write(tweet.content)
        
#df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
#st.write(df)

# to save to csv
# df.to_csv('tweets.csv')

CSV_FILE = "newest_products.csv"
TOTAL_PRODUCTS_TO_GET = 50
Titles = []
Titles_Set = set()
Urls = []
Urls_Set = set()
Description_Set = set()
Descrip = []
CompleteSet = [[]]
Images = []
imageSet = set()
product_id_arr = []

def parse_html(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    return soup

def get_unique_id(url):
    # Extract a unique identifier from the URL
    match = re.search(r'/posts/(\d+)', url)
    if match:
        return match.group(1)
    else:
        return ''

def scrape_newest_products():
    products = []
    soup = parse_html("https://www.producthunt.com/newest")
    links = soup.find_all('a', href=lambda href: href and href.startswith('/posts/'))
    for link in links:
        product_url = "https://www.producthunt.com" + link['href']
        product_title = link.text.strip()
        #product_description = link.text.strip()


        # Find the element containing the description
        #description_element = link.find_next_sibling('div')  # Example: Assuming the description is a sibling paragraph
        
        #description_element = link.find('a')

        # Extract the description text
        #if description_element:
        #    product_desc = description_element.text.strip()
         #   if product_desc not in Description_Set: 
        #        Description_Set.add(product_desc)
        #       Descrip.append(product_desc)
       #else:
          #  product_desc = ""


         # Get the unique identifier for the product
        product_id = get_unique_id(product_url)
        product_id_arr.append(product_id)

        if product_title not in Titles_Set: 
            Titles_Set.add(product_title)
            Titles.append(product_title)
        if product_url not in Urls_Set: 
            Urls_Set.add(product_url)
            Urls.append(product_url)

        

        #Trying to the get the image: 
        image_element = link.find_previous('img')  # Modify this line based on the specific structure

        # Find the image associated with the product using the unique identifier
        #image_element = soup.find('img', attrs={'alt': product_id})  # Modify this line based on the specific structure

        # Extract the image source URL
        if image_element:
            image_url = image_element['src']
            if image_url not in imageSet: 
                imageSet.add(image_url)
                Images.append(image_url)
        else:
            image_url = ""


         #CURRENT WORKING: ""
        #if (product_title not in Titles_Set) and (product_url not in Urls_Set): # and (product_description not in Description_Set
         #   Titles_Set.add(product_title)
         #   Urls_Set.add(product_url)
            #Description_Set.add(product_description)
         #   CompleteSet.append([product_title, product_url]) ""


        #if product_title: 
        #st.write("Title" + product_title) #Added
        #if product_url: 
        #st.write("URL" + product_url) #Added
        products.append({'Title': product_title, 'URL': product_url})
        if len(products) == TOTAL_PRODUCTS_TO_GET:
            break

    Titles.pop(0)
    Titles.pop(-1)
    Urls.pop(-1)

    popped_indices = []

    # Iterate over the Titles array in reverse order
    for i in range(len(Titles) - 1, -1, -1):
        if (i + 1) % 2 == 0:  # Check if the index is even (every second element)
            popped_indices.append(i)

    # Create a new array to store the updated Titles
    updated_titles = [Titles[i] for i in range(len(Titles)) if i not in popped_indices]

    # Create a new array to store the popped elements
    popped_elements = [Titles[i] for i in popped_indices]

    popped_elements.reverse()

    st.write("")
    st.write("")
    st.write("")

    for i in range(len(updated_titles) - 1): 
        current = i+1
        cur_str = str(current)
        st.write(cur_str + ". Title: " + updated_titles[i])
        st.write("Description: " + popped_elements[i])
        st.write("URL: " + Urls[i])
        st.write("")
        st.write("")

    st.write("")
    st.write("")
    st.write("")

    if Images: 
        for image in Images: 
            st.write(image)
    
    st.write("")
    st.write("")
    st.write("")

    #printing out the product-ID's - Currently, all product ID's are empty so this doesn't work
    for q in product_id_arr: 
        st.write(q)

    st.write("")
    st.write("")
    st.write("")

    return products

def save_to_csv(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title ', 'URL'])
        writer.writeheader()
        writer.writerows(data)

try:
    newest_products = scrape_newest_products()
    save_to_csv(newest_products)
    print("Data has been successfully scraped and saved to", CSV_FILE)
except Exception as e:
    print("An error occurred:", str(e))