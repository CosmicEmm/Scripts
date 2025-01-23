from selenium import webdriver  # For automating the browser
from selenium.webdriver.common.by import By  # To locate elements
from selenium.webdriver.common.keys import Keys # To simulate keyboard keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException # To handle exceptions related to timeouts
from selenium.webdriver.support.wait import WebDriverWait # To implement explicit waits
from selenium.webdriver.support import expected_conditions as EC # To specify the expected conditions for the explicit waits
from sys import argv  # To access command-line arguments
import time  # To add pauses between actions
import logging
import subprocess # To run shell commands from within the Python script

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Check if the user has provided the name of the anime and the episode number as command-line arguments
if len(argv) < 2:
    print("Please provide the name of the anime")
    exit(1)
elif len(argv) < 3:
    print("Please provide the episode number")
    exit(1)

def gogo_anime(anime, episode_no):
    # Initialize browser options for Microsoft Edge
    options = webdriver.EdgeOptions()

    # Specify the location of the uBlock Origin extension
    ublock_origin = r'F:\Extensions\uBlock Origin.crx'
    # ublock_origin = os.path.abspath(r'F:\Extensions\uBlock Origin.crx')
    options.add_extension(ublock_origin)

    # Modify the browser settings to disable images (helps speed up loading and saves bandwidth)
    options.add_argument("--blink-settings=imagesEnabled=false")

    # options.add_argument("--headless") # Run the browser in headless mode (without opening a window)
    
    # Launch the Edge browser with the specified options (including extensions and settings)
    driver = webdriver.Edge(options=options)

    # Wait for 10 seconds to ensure the uBlock Origin extension is fully loaded
    time.sleep(10)

    # Set the global page load timeout for the session. If the page takes longer than 40 seconds to load, a TimeoutException will be raised
    driver.set_page_load_timeout(40)
    
    # Set the implicit wait time for the driver. This will be applicable for all the elements located by the driver
    driver.implicitly_wait(5)

    # Step 1: Load the GoGoAnime website
    try:
        logging.info("Loading the GoGoAnime website...")
        driver.get('https://ww19.gogoanimes.fi/')
    except TimeoutException:
        pass # Continue to the next step even if the website takes longer than 40 seconds to load
    finally:
        logging.info("Website Loaded!") # Log a message indicating that the website has been loaded successfully

    
    try:
        # Step 2: Locate the search input box and enter the anime name
        logging.info("Locating the search input box...")
        search_box = driver.find_element(By.ID, "keyword")
        logging.info("Search box located, typing anime name...")
        search_box.send_keys(f'{anime}')
    
        # Step 3: Initiate the search by simulating the Enter key press
        logging.info("Loading search results...")
        search_box.send_keys(Keys.ENTER)
    except NoSuchElementException:
        logging.error("Unable to locate the search box")
        driver.quit()
        return None
    except TimeoutException:
        pass

    
    try:
        # Step 4: Click on the first search result
        logging.info("Clicking the first search result to proceed to the episodes directory...")
        search_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul > li:nth-child(1) > p.name > a'))) #"p.name a"
        search_result.click()
    
        # Step 5: Locate and click on the specific episode
        logging.info("Locating the specific episode...")
        # nth-last-child is a pseudo-class that locates elements based on their position as a child of a parent, counting from the end.
        episode = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#episode_related > li:nth-last-child({episode_no}) > a")))
        episode.click()
    
        # Step 6: Click on the download button for the episode
        logging.info("Clicking the download button to access the download links...") # 'li.dowloads a'
        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.favorites_book > ul > li.dowloads > a")))
        download_button.click()
        
        # Step 6: Switch to the download window and extract the download link
        logging.info("Switching to the download window...")
        download_window = driver.window_handles[-1]
        driver.switch_to.window(download_window)
        logging.info("Extracting the 1080p download link...") # '//div[@class="dowload"]/a[contains(text(), "1080P - mp4")]'
        Mp4_1080p = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-download > div:nth-child(1) > div:nth-child(6) > a")))
        download_link = Mp4_1080p.get_attribute('href') # Extract the download link
        logging.info("Download link successfully extracted!")
        
    except TimeoutException:
            logging.error(f"Timeout during element interaction")
            driver.quit()
            return None # Return None if the timeout exception occurs
    
    
    # Close the browser session
    print("Closing the browser session...")
    driver.quit()
    return download_link # Return the download link


# Call the function
link = gogo_anime(anime=argv[1], episode_no=argv[2])
print(link)

# Check if the download link was successfully extracted
if link is None:
    exit(1)
else:
    pass # Continue to the next step

destination_folder = 'F:/Anime'

# Constructing the command to launch IDM to start downloading the episode from the link and save it in the destination folder
command = f'idman.exe /d "{link}" /p "{destination_folder}" /f "{argv[1]}"-EP"{argv[2]}".mp4'

# Running the above command in the shell from within the Python script
subprocess.run(command, shell=True)