from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import os
import sys

# Redirect stderr to the null device
#sys.stderr = open(os.devnull, 'w')

# Replace this with the URL of the website you want to scrape
url='https://mean-ways-grow-35-247-178-248.loca.lt/#'
# Replace this with the path to your Chrome driver executable
driver_path = "/path/to/chromedriver"

# Initialize the Chrome driver
driver = webdriver.Chrome(driver_path)

# Load the website
driver.get(url)

wait = WebDriverWait(driver, 5)

# Find the input element and submit button element
#input_field = wait.until(EC.presence_of_element_located((By.ID, "inputfield")))
input_element = driver.find_element(By.ID, "input_text")
submit_button = driver.find_element(By.ID, "btnsend")

# define the initial value of last_message
last_message = ""

# Loop to interact with the bot
def wait_for_bot_response(driver, last_message):
    """
    Wait for the bot to respond with a new message on the web page.

    :param driver: The Selenium WebDriver instance.
    :param last_message: The last message received from the bot.
    :return: The new message from the bot.
    """
    # wait for the latest message element to appear
    latest_message_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div[1]/span/chunk[last()]"))
    )

    # get the text content of the latest message element
    latest_message_text = latest_message_element.text

    # check if the latest message is different from the last message
    if latest_message_text.startswith("Atsushi Nakajima: ") and latest_message_text != last_message:
        return latest_message_text.split("Atsushi Nakajima: ")[1]
    else:
        # wait for a new message
        time.sleep(1)
        return wait_for_bot_response(driver, last_message)



while True:
    # Wait for the bot to respond
    latest_message_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div[1]/span/chunk[last()]"))
        
    # Get user input
    user_input = input("Enter your message: ")

    # Enter user input in input element and click the submit button
    input_element.send_keys(user_input)
    submit_button.click()
    
    # Enter user input in input element and click the submit button
    bot_response = wait_for_bot_response(driver, last_message)
    last_message = "Atsushi Nakajima: " + bot_response
    if last_message != bot_response:
        print("Bot: ", last_message)
        continue
    else:
        continue
    ## Wait for the bot to respond
    #bot_response = wait_for_bot_response(driver, last_message)
    #last_message = "Atsushi Nakajima: " + bot_response
    #print("Bot: ", bot_response)
    #WebDriverWait(driver, 0.1).until(EC.staleness_of(last_message))
