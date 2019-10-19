from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import json 
from keyword_tree import KeywordTree

messages = {
    "INVALID_COMMAND": "Please enter the command in below format:\npython3 enroll.py -u [username] -p [password]"
}

course_info = {}
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

def get_semester_no(year, season):
    year = str(year)
    return (year + '1') if (season == 'fall' or season == 'winter') else str(int(year) - 1) + '2' if season == 'spring' else str(int(year) - 1) + '3'

def get_course_info():
    global course_info

    course_name = driver.find_element_by_xpath('//h3[@class="coursename"]/a').text

    course_info["course_words"] = [word for word in course_name.split() if word.isalpha()]
    course_info["course_name"] = ' '.join(course_info["course_words"])
    course_info["first_letters"] = [word[0] for word in course_info["course_words"]]
    course_info["acronym"] = ''.join(course_info["first_letters"])
    course_info["season"], course_info["year"]= driver.title.split()[-2].lower(), driver.title.split()[-1]
    course_info["semester_no"] = '1' if course_info['season'] == 'fall' else '2' if course_info['season'] == 'spring' else '3' if course_info['season'] == 'summer' else '1'
    course_info["semester_year"] = course_info['year'] if course_info['season'] == 'fall' else str(int(course_info['year']) - 1)
    
    print(course_info)

def try_to_enroll(enrollment_key):
    print ("Trying to enroll with key '" + enrollment_key + "'")
    enroll_field = driver.find_element_by_xpath('//input[@name="enrolpassword"]')
    enroll_field.clear()
    enroll_field.send_keys(enrollment_key)
    enroll_field.send_keys(Keys.ENTER)

def enroll(course_url):
    driver.get(course_url)
    get_course_info()
    keyword_tree = KeywordTree(course_info)
    key_list = keyword_tree.gen_key_list()

    for enrollment_key in key_list:
        try_to_enroll(enrollment_key)
        if "cecm.ut.ac.ir/enrol" not in driver.current_url:
            exit("Enrolled with success! Key: '" + enrollment_key + "'")
        else: print ("FAIL!")
    
    print ("Failed to enroll :(")
    

def main():
    global config
    config = read_config('config.json')
    update_config(config, sys.argv)
    setup_driver()
    login()
    enroll(config["course_url"])



if __name__ == "__main__":
    main()
