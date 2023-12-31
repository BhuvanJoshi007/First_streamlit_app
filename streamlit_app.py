import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new edited healthy dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# To display fruityvice API response
# import requests

# streamlit.header("Fruityvice Fruit Advice!")
# CODE FROM  LINE 32 TO 40) IS COMMENTED and is changed from to try except block because we want a certain set of code to execute without affecting the snowflake data base
# -- fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# -- streamlit.write('The user entered ', fruit_choice)

# -- fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# This command will flatten the JSON content into a tabular form
# -- fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# This will display the dataframe
# -- streamlit.dataframe(fruityvice_normalized)

# Introducing this structure allows us to separate the code that is loaded once from the code that should be repeated each time a new value is entered.

# now we will contain the comment the code from line 45 to 55 and add it to a function
#try:
#  fruit_choice = streamlit.text_input('What fruit would you like information about?')
#  if not fruit_choice:
#    streamlit.error("Please select a fruit to get information.")
#  else :
#    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
#    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#    streamlit.dataframe(fruityvice_normalized)
#
# except URLError as e:
#  streamlit.error()

# Create a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
# do not run anything beyond this line, resulting in no output in the streamlit application.
#- streamlit.stop()

# import snowflake.connector --- Now commented to be converted to function
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("View Our Fruit List- Add Your Favourite!:")
#streamlit.dataframe(my_data_rows)

streamlit.header("View Our Fruit List- Add Your Favourite!:")
# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


## This code from line 100 to 104 will also be commented and changed to a function
# Add A Second Text Entry Box
#fruit_choice_2 = streamlit.text_input('What fruit would you like to add?','jackfruit')
#streamlit.write('Thanks for adding ', fruit_choice_2)
#
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

#Allows the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)
