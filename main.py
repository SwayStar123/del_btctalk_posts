import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def extract_ids_from_url(post_url):
    # Splitting the URL based on "?"
    parameters = post_url.split('?')[1]
    
    # Extracting topic and msg IDs from the parameters
    topic_id = parameters.split('.msg')[0].split('topic=')[1]
    msg_id = parameters.split('.msg')[1].split('#')[0]
    
    return topic_id, msg_id

def delete_post(browser, post_url, sesc_token):
    topic_id, msg_id = extract_ids_from_url(post_url)
    
    # Constructing the delete URL
    delete_url = f"https://bitcointalk.org/index.php?action=deletemsg;topic={topic_id}.0;msg={msg_id};sesc={sesc_token}"

    browser.get(delete_url)

    time.sleep(1)

    if browser.current_url == f"https://bitcointalk.org/index.php?topic={topic_id}.0":
        return True
    else:
        return False

def edit_post(browser, post_url, sesc_token):
    topic_id, msg_id = extract_ids_from_url(post_url)
        
    # Navigate to edit URL
    edit_url = f"https://bitcointalk.org/index.php?action=post;msg={msg_id};topic={topic_id}.0;sesc={sesc_token}"
    browser.get(edit_url)
    
    try:
        # Change the subject to "x"
        subject_elem = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.NAME, 'subject'))
        )
        subject_elem.clear()
        subject_elem.send_keys('x')
        
        # Change the message content to "x"
        message_elem = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.NAME, 'message'))
        )
        message_elem.clear()
        message_elem.send_keys('x')
        
        # Click the Save button
        save_button = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.NAME, 'post'))
        )
        save_button.click()
        
    except Exception as e:
        print(f"Error editing post: {e}")
    
    time.sleep(0.5)  # Introduce a delay before processing the next post or action


def scrape_post_urls(browser, start):
    browser.get(BASE_URL + str(start))
    post_urls = []
    try:
        # Target <a> elements within <td> of class 'middletext' and get the third (last) link
        post_elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//td[@class="middletext"]/a[3]'))
        )
        for post_element in post_elements:
            post_urls.append(post_element.get_attribute("href"))
    except Exception as e:
        print(f"Error scraping post URLs at start={start}: {e}")
    return post_urls

def extract_sesc_token(browser):
    # Go to the homepage or any page where the logout link is visible
    browser.get("https://bitcointalk.org/index.php")
    try:
        # Locate the logout link and extract the sesc token from its href attribute
        logout_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "action=logout")]'))
        )
        href = logout_link.get_attribute('href')
        sesc_token = href.split('sesc=')[1]
        return sesc_token
    except Exception as e:
        print(f"Error extracting sesc token: {e}")
        return None

def extract_user_id(browser):
    # Navigate to main profile page
    browser.get('https://bitcointalk.org/index.php?action=profile')
    
    try:
        # Extracting the URL of the 'Account Related Settings' link
        account_related_settings_url = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Account Related Settings")]'))
        ).get_attribute('href')
        
        # Extracting the user ID from the URL
        user_id = re.search(r'u=(\d+)', account_related_settings_url).group(1)
        return user_id
    
    except (TimeoutException, AttributeError):
        print("Failed to extract user ID.")
        return None
    
if __name__ == '__main__':
    num_pages = int(input("How many pages of posts do you have in your profile?: "))

    browser = webdriver.Chrome()

    # Navigate to login page or homepage
    browser.get("https://bitcointalk.org/index.php?action=login")
    print("Please login manually within the next 60 seconds...")
    time.sleep(60)  # Give 60 seconds for manual login

    # Extract user ID
    user_id = extract_user_id(browser)

    if not user_id:
        print("Failed to extract user ID.")
        browser.quit()
        exit()

    BASE_URL = f'https://bitcointalk.org/index.php?action=profile;u={user_id};sa=showPosts;start='

    sesc_token = extract_sesc_token(browser)
    if sesc_token:
        print(f"Extracted sesc token: {sesc_token}")

        # Continue with rest of your logic, e.g., scraping post URLs and deleting posts
        all_post_urls = []
        for start in range(0, num_pages*20, 20):
            all_post_urls.extend(scrape_post_urls(browser, start))

        for post_url in all_post_urls:
            res = delete_post(browser, post_url, sesc_token)
            if res == True:
                continue
            else:
                edit_post(browser, post_url, sesc_token)
    else:
        print("Failed to extract sesc token.")
    
    browser.quit()
