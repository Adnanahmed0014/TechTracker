import requests
import streamlit as st
from PIL import Image
# Import the app function from login_system.py
from login_system import app as login_app
import tweepy 
import re 
import snscrape.modules.twitter as sntwitter
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import xlwt 
from xlwt import Workbook
import csv
from ProductsContainer import scrape_newest_products as display_products


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

#Run app in Terminal - streamlit run Home.py

def displayy_products():
    # Move the code from 'products.py' here
    st.title("Products")
    st.subheader("Newest tech: ")
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
            OLD - st.write(cur_str + ". Title: " + updated_titles[i])
            OLD - st.write("Description: " + popped_elements[i])
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








# Function to display the Home page
def home_page():
    st.title("Home")
    st.sidebar.success("Select a page above.")

    with st.container():
        st.subheader("Hi, I am Adnan :wave:")
        st.title("A Computer Science Student at Rutgers University")
        st.write(
            "I am passionate about finding ways to use Python and VBA to be more efficient and effective in business settings."
        )
        st.write("[Learn More >](https://pythonandvba.com)")

# Function to display the Login page
def login_page():
    login_app()  # Call the login_app function from login_system.py

# Main function to run the app
def main():
    # Define pages to navigate
    pages = {"Home": home_page, "Login": login_page}

    # Display the sidebar navigation options
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", list(pages.keys()))

    # Navigate to the selected page
    #pages[page]()
    #New Change otherwise it was just the line above: 
    if st.session_state.get('logged_in', False):
        # Display the personalized greeting
        username = st.session_state.get('username', '')
        st.sidebar.write(f"Logged in as: {username}")
        if page == "Home":  # If the user is on the Home page, show the products page
            displayy_products()
            #display_products()  # Call the function to display the products page from the 'pages' folder
        else:  # For other pages, show the selected page
            pages[page]()
    else:
        # Navigate to the selected page
        pages[page]()

# Run the app
if __name__ == "__main__":
    main()