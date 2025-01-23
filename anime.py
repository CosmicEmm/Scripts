from playwright.sync_api import Playwright, sync_playwright, TimeoutError
from sys import argv   # To handle command-line arguments
import subprocess      # To run shell commands and manage external processes directly from within the Python script
import logging         # For logging messages


# Configure logging to display messages with timestamps and log levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def argv_check() -> bool:
    """
    Checks and validates the command-line arguments provided by the user.
    Returns the browser mode (headless or headed) as a boolean.
    """
    if len(argv) < 2:   # Check if anime name is provided
        print("Please provide the name of the anime")
        exit(1)   # Non-zero status indicates an error or abnormal termination
    elif len(argv) < 3:   # Check if episode number is provided
        print("Please provide the episode number")
        exit(1)
    elif len(argv) < 4:   # Check if browser mode is provided
        try:
            int(argv[2])   # Validate if episode number is an integer
            print('Specify the browser mode: 1 for Headless; 0 for Headed')
        except ValueError:
            print("Invalid episode number. Please provide a valid integer.")
        finally:
            exit(1)
    else:
        if argv[3] not in ['0', '1']:   # Validate browser mode (0 or 1)
            print("Invalid browser mode. Use 1 for headless or 0 for headed.")
            exit(1)
        mode = bool(int(argv[3]))   # Convert browser mode to boolean (1 -> True, 0 -> False)
    
    return mode   # Return the browser mode
    
# The colons (:) are used to specify the expected data types of the function's parameters
def run(
        playwright: Playwright,  # playwright parameter is expected to be an instance of the Playwright class
        anime: str,
        episode_no: int,
        browser_mode: bool
    ) -> str:
    """
    Extracts the download link for the specified episode of an anime using Playwright.
    
    Args:
        playwright (Playwright): An instance of the Playwright class.
        anime (str): The name of the anime.
        episode_no (int): The episode number.
        browser_mode (bool): Determines the browser mode (headless or headed)
    
    Returns:
        str: Extracted download link
    """
    # Define paths for browser user data and extensions
    userDataDir = 'F:\\UserData\\Chrome'   # Directory for Chrome user data
    extension_path = r'F:\\UserData\\uBlock Origin'   # Path to uBlock Origin extension (extracted)
    
    # List of arguments for the args parameter of the lauch_persistent_context method
    arg_list=[f'--disable-extensions-except={extension_path}', f'--load-extension={extension_path}']   # disable all extensions except uBlock Origin and load it

    if browser_mode:   # Add --headless flag if browser_mode is True (1)
        arg_list.append('--headless')

    # Launch a persistent browser with the specified behavior
    browser = playwright.chromium.launch_persistent_context(
        userDataDir,
        headless=False,   # Default to headed mode, but --headless in args take precedence
        channel='chrome', # Use the official Chrome browser
        args=arg_list     # Pass the list of arguments to the browser instance
    )
    
    page = browser.pages[0]   # Use the first available page in the browser

    try:
        # Navigate to the GOGOAnime website
        logging.info('🌐 Setting sail to the GOGOAnime website... Hold on tight!')
        page.goto("https://ww19.gogoanimes.fi/")
        logging.info('🚀 Website successfully loaded! Ready for the adventure to begin!')

        # Search for the anime
        page.locator('[placeholder="search"]').click()
        logging.info("🧐 Inputting search query... Let's find that anime!")
        page.locator('[placeholder="search"]').fill(f"{anime}")
        page.locator('[onclick="do_search();"]').click()
        logging.info('🌀 Sifting through the vast animeverse...')
        logging.info('🎯 Aha! Found the one you were looking for! Great choice!🔥')

        # Select the first search result
        page.locator('ul > li:nth-child(1) > p.name > a').click()
        logging.info('📜 Loading the episode list... Almost there!')
        logging.info("✅ Episode list loaded! Let’s see what we have!")

        # Locate and click on the specified episode
        logging.info(f"🔍 Locating episode {episode_no}... It’s got to be here somewhere!")
        page.locator(f"#episode_related > li:nth-last-child({episode_no}) > a > div.name").click()
        logging.info('🙌 Episode found! The quest continues!')
        
        # Extract the URL for the download directory
        download_url = page.locator("div.favorites_book > ul > li.dowloads > a").get_attribute('href')
    except TimeoutError:
        logging.error('⏰ Uh-oh! The operation timed out!')
        logging.info('🛑 Closing the browser...Time to regroup and try again later!')
        browser.close()
        exit(1)
    
    try:
        # Navigate to the download directory
        logging.info('⏳ Navigating to the download directory... Please wait, the treasure is almost yours!')
        page.goto(download_url)
    except TimeoutError:   # Ignore timeout error
        pass
    
    try:
        # Extract the 1080P download link
        logging.info('🔑 Extracting the 1080P download link... The magic is happening!')
        link_element = page.locator("#content-download > div:nth-child(1) > div:nth-child(6) > a")
        href = link_element.get_attribute('href')
        logging.info('🎉 Yatta! Download link successfully extracted! You did it!')
        logging.info('🎬 Your anime adventure is about to begin! Grab your snacks! 🍿')
        logging.info('👋 Until next time, stay awesome and keep watching!')
    except TimeoutError:
        # Log an error if the download link cannot be extracted and return None
        logging.error('🕒 Oops! The download link is playing hard to get. Try again later!')
        return None
    except Exception as e:
        # Log any other unexpected errors
        logging.error(f'❌ An unexpected error occurred: {e}')
        return None
    finally:
        # Close the browser regardless of whether the link extraction succeeds or fails
        browser.close()
        logging.info('🛑 Browser closed')
    
    
    return href   # Return the extracted download link


# Store the return value (bool) from the argv_check function in a variable
mode = argv_check()

# Call the main automation function and store its return value in the url variable
with sync_playwright() as playwright:
    url = run(
             playwright,         # Pass the Playwright instance to the `run` function
             anime=argv[1],      # Anime name from command-line arguments
             episode_no=argv[2], # Episode number from command-line arguments
             browser_mode=mode   # Browser mode (headless or headed) from the argv_check function
        )

# Exit the program if no download URL is extracted, otherwise continue
if url is None:
    exit(1)   
else:
    pass

# Define paths for Internet Download Manager (IDM) and destination folder
idm_path = r'"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"'
destination_folder = 'F:/Anime'

# Construct the IDM shell command to download the anime episode from the extracted link
idm = f'{idm_path} /d "{url}" /p "{destination_folder}" /f "{argv[1]}"-EP"{argv[2]}".mp4'

# Execute the IDM shell command from within the Python script
subprocess.run(idm, shell=True)