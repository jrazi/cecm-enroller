from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import json 


messages = {
    "INVALID_COMMAND": "Please enter the command in below format:\npython3 enroll.py -u [username] -p [password]"
}
driver = None
config= {}

def exit(message):
    print(message)
    sys.exit()

def read_config(file_name):
    with open(file_name) as config_file:
        config = json.load(config_file)
        return config

def update_config(config, argv):
    config["user_info"] = {}
    if '-u' in sys.argv:
        index = sys.argv.index('-u')
        config["user_info"]['username'] = [sys.argv[index+1]]
    else: exit(messages['INVALID_COMMAND'])

    if '-p' in sys.argv:
        index = sys.argv.index('-p')
        config["user_info"]['password'] = sys.argv[index+1]
    else: exit(messages['INVALID_COMMAND'])


def setup_driver():
    global driver
    driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')

def login():
    driver.get(config['login_url'])
    username_field = driver.find_element_by_xpath('//input[@id="usename-field"]')
    password_field = driver.find_element_by_xpath('//input[@id="password"]')
    username_field.send_keys(config['user_info']['username'])
    password_field.send_keys(config['user_info']['password'])
    password_field.send_keys(Keys.ENTER)

def enroll(course_url):
    driver.get(course_url)

def main():
    global config
    config = read_config('config.json')
    update_config(config, sys.argv)
    setup_driver()
    login()
    enroll(config["course_url"])



if __name__ == "__main__":
    main()
