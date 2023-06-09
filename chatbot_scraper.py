from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import os
import sys

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

# Redirect stderr to the null device
#sys.stderr = open(os.devnull, 'w')

# This is a Dynamic way where the code asks for the url at startup
url = input("Enter your url: ")
botname = input("Enter your botname (eg: Alexa:) !add the colons ":" and this is case sensitive")
#^
# the url is can be of both inputted using both ways disable the either one
#
# Replace this with the URL of the website you want to scrape
#url='https://plenty-experts-decide-35-204-120-216.loca.lt/#'
# Replace this with the path to your Chrome driver executable
driver_path = "/path/to/chromedriver"

# Initialize the Chrome driver
driver = webdriver.Chrome(driver_path,options=op)

# Load the website
driver.get(url)

# Find the input element and submit button element
input_element = driver.find_element(By.ID, "input_text")
submit_button = driver.find_element(By.ID, "btnsend")

# define the initial value of last_message
lastest_message_text = ""


def log_conversation(conversation):
    with open("conversation_log.txt", "a") as file:
        file.write(conversation)
        file.write("\n")

def check_if_message_exists(message):
    with open("conversation_log.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if message in line:
                return True
    return False

def wait_for_bot_response(driver, last_message,botname):
    while True:
        # get the latest message element
        latest_message = driver.find_element(By.XPATH ,"/html/body/div[1]/div[5]/div[1]/span/chunk[last()]")
        
        # get the text content of the latest message
        latest_message_text = latest_message.text
        
        # check if the latest message is from the bot and not the user
        if latest_message_text.startswith(botname) and latest_message_text != last_message:
            message = latest_message_text.split(": ")[1]
            
            # check if the message has already been processed before
            if not check_if_message_exists(message):
                log_conversation(latest_message_text)
                return message
        
        # wait for 1 second before checking again
        time.sleep(1)


# Loop to interact with the bot
log_file = "conversation_log.txt"
previous_messages = set()

while True:
    latest_message_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div[1]/span/chunk[last()]")))

    # get user input
    user_input = input("Enter your message: ")
    
    # check if the user input has already been said before
    #if user_input in previous_messages:
    #    print("Bot: I'm sorry, I don't want to repeat myself.")
    #    continue
    
    # add user input to previous messages
    previous_messages.add(user_input)
    
    # send user input to bot
    #send_message(user_input)
    input_element.send_keys(user_input)
    submit_button.click()

    latest_message_text = driver.find_element(By.XPATH ,"/html/body/div[1]/div[5]/div[1]/span/chunk[last()]")

    # wait for bot response
    bot_response = wait_for_bot_response(driver, latest_message_text)
    
    # check if bot response has already been said before
    if bot_response in previous_messages:
        print(botname+" I'm sorry, I don't want to repeat myself.")
        continue
    
    # add bot response to previous messages
    previous_messages.add(bot_response)
    
    # log conversation to file
    with open(log_file, "a") as f:
        f.write(f"You: {user_input}\n")
        f.write(f"{botname} {bot_response}\n")
    
    # print bot response
    print(botname, bot_response)

