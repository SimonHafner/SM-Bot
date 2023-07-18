import time
import os
import fileinput
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def save_credentials(username, password):
    with open("credentials.txt", "w") as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    if not os.path.exists("credentials.txt"):
        return None

    with open("credentials.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None


def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password


def read_usernames_from_file(file_path):
    with open(file_path, "r") as file:
        usernames = [line.strip() for line in file]
    return usernames

def remove_username_from_file(username, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != username:
                file.write(line)


def like_stories(username, password, usernames):
    # Set up ChromeDriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration



    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Set up ChromeDriver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Warten Sie eine Weile, bis die Seite geladen ist
    wait = WebDriverWait(driver, 20)

    # Navigieren Sie zur Instagram-Anmeldeseite
    driver.get("https://www.instagram.com/accounts/login/")

    # Cookie-Banner schließen
    try:
        # Finden Sie den Button auf Basis des CSS-Selektors und klicken Sie darauf
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="_a9-- _a9_0"]')))
        button.click()
    except Exception as e:
        print(f"Couldn't click the cookie button. {e}")
    
    print("Clicked on 'Accept all cookies'")

    # Finden Sie das Eingabefeld für den Benutzernamen
    try:
      username_field = WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    except Exception as e:
        print(f"Couldn't extract input field for username.")

    # Geben Sie den Benutzernamen ein
    username_field.send_keys(username)
    
    try:
    # Finden Sie das Eingabefeld für das Passwort
      password_field = WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    except Exception as e:
      print(f"Couldn't extract input field for password. {e}")

    # Geben Sie das Passwort ein
    password_field.send_keys(password)

    # Finden Sie den Anmelde-Button und klicken Sie darauf
    try:
      login_button = WebDriverWait(driver, 100).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    except Exception as e:
        print(f"Couldn't extract submit button from page. {e}")
    
    # Use JavaScript to click the button
    driver.execute_script("arguments[0].click();", login_button)

    # Warten Sie eine Weile, bis die Anmeldung verarbeitet wurde
    WebDriverWait(driver, 90).until(EC.staleness_of(login_button))
    print("Login successful!")

    # Like stories of each follower
    for follower in usernames:
      story_url = f"https://www.instagram.com/stories/{follower}"
      driver.get(story_url)
      time.sleep(2)
      print("Inspecting userpage of '" +str(follower) +"'")

      # Hypothetical CSS selector for the "View Story" button
      # view_story_css_selector = "div.section"
      
      try:
        like_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x6s0dn4.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1ypdohk.x78zum5.xl56j7k.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha'))
        )
        driver.execute_script("arguments[0].click();", like_button)
        print("Liked the story successfully!")

      except NoSuchElementException:
          print("Failed to like the story.")
          continue

         

          # Hypothetical CSS selectors for the like button
          like_button_css_selector_1 = "div.likeButton1"
          like_button_css_selector_2 = "div.likeButton2"

          try:
              like_button = WebDriverWait(driver, 20).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, like_button_css_selector_1))
              )
              # Click on the like button or perform desired action
              like_button.click()
              print("Liked the story successfully!")
          except NoSuchElementException:
              try:
                  like_button = WebDriverWait(driver, 120).until(
                      EC.presence_of_element_located((By.CSS_SELECTOR, like_button_css_selector_2))
                  )
                  # Click on the like button or perform desired action
                  like_button.click()
                  print("Liked the story successfully!")
              except NoSuchElementException:
                  # Both CSS selectors failed, skip to the next action or user
                  print("Failed to like the story.")
                  continue  # Assuming this is inside a loop

      except NoSuchElementException:
          print("[FALSE] User -> " + follower + " has no story up.")
          continue
    remove_username_from_file(follower, followers_file)

    # Close the ChromeDriver instance
    driver.quit()


if __name__ == "__main__":
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    followers_file = "followers.txt"
    usernames = read_usernames_from_file(followers_file)

    like_stories(username, password, usernames)
