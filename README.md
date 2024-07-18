# RecaptchaV2-Bypass-Solve-using-Selenium-Python-and-TamperMonkey-ViolentMonkey
![Tamper_Monkey-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d9de97ee-1396-4977-bf5c-db7eb0df402a)

Automating tasks in web browsers can significantly improve productivity and efficiency. One powerful way to achieve this is by using TamperMonkey or ViolentMonkey to inject custom JavaScript into web pages. In this article, we will walk through a detailed process of bypassing or solving RecaptchaV2 using Selenium in Python. By the end of this guide, you will be able to load a JavaScript file into TamperMonkey or ViolentMonkey using Selenium, making your automation scripts even more powerful.

**Important Steps:**
Download Extension : [Chrome_Extension_Link](https://chromewebstore.google.com/detail/crx-extractordownloader/ajkhmmldknmfjnmeedkbkkojgobmljda)

Then go to ViolentMonkey or TamperMonkey Extension on chrome web store : [Click Here](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)

Now download the extension zip file by clicking on CRX extractor Extension "Download as Zip"

Extract that zip and put the path of extension folder into the code below.

**Prerequisites**

- Basic knowledge of Python and JavaScript.
- Chrome browser installed.
- TamperMonkey or ViolentMonkey extension installed.
- Selenium WebDriver and seleniumbase installed.

Step-by-Step Guide

Let's break down the process step-by-step. Here is the complete code followed by an explanation of each section.

```python
import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Initialize and configure the WebDriver
print("Starting Driver")
driver = Driver(uc=True, extension_dir="extensions/Tampermonkey")  # Replace your extension directory here
driver.maximize_window()

# Wait for the extension tab to close
time.sleep(4)

# Close any additional tabs that opened during the initialization
while True:
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    else:
        driver.switch_to.window(driver.window_handles[-1])
        break

# Open Chrome extension settings
driver.uc_open("chrome://extensions/")

# Wait for the extensions manager to load
wait = WebDriverWait(driver, 10)
extensions_manager = wait.until(EC.presence_of_element_located((By.TAG_NAME, "extensions-manager")))

# Access the shadow DOM of the extensions manager
shadow_root1 = driver.execute_script("return arguments[0].shadowRoot", extensions_manager)

shadow_root2 = shadow_root1.find_element(By.CSS_SELECTOR, '#toolbar')
shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", shadow_root2)

shadow_root3 = shadow_root2.find_element(By.CSS_SELECTOR, '#devMode')
shadow_root3.click()

# Get the extension ID of TamperMonkey or ViolentMonkey
view_manager = shadow_root1.find_element(By.ID, "items-list")
shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", view_manager)

extensions = shadow_root2.find_element(By.CSS_SELECTOR, "#extensions-section > div")
all_extensions = extensions.find_elements(By.XPATH, ".//*")

extension_id = all_extensions[0].get_attribute("id")

# Refresh the extension to ensure it's fully loaded
shadow_root4 = driver.execute_script("return arguments[0].shadowRoot", all_extensions[0])
reload_extension = shadow_root4.find_element(By.CSS_SELECTOR, "#dev-reload-button")
reload_extension.click()

time.sleep(2)

# Close any additional tabs that opened during the reload
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
else:
    driver.switch_to.window(driver.window_handles[0])

# Visit the extension's options page to add a new user script
driver.uc_open(f"chrome-extension://{extension_id}/options.html#nav=new-user-script+editor")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".CodeMirror"))
)

# Load the JavaScript to be added from a text file
with open("Recaptcha.txt", "r", encoding="utf-8") as file:  # Replace with your script file
    new_text = file.read()

# Inject the script content into the CodeMirror editor
driver.execute_script("""
    var editor = document.querySelector('.CodeMirror').CodeMirror;
    editor.setValue(arguments[0]);
    editor.refresh();
""", new_text)

time.sleep(1)

# Save the script using the keyboard shortcut (Ctrl+S)
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()

# Test the script by navigating to a target web page
driver.uc_open("https://www.google.com/recaptcha/api2/demo")
```

**Code Explanation***

1. **Initialize and Configure the WebDriver:**
    - Import necessary libraries.
    - Start the WebDriver with `uc=True` for undetected mode and specify the extension directory.
    - Maximize the browser window.

2. **Handle Extension Tab:**
    - Wait for a few seconds to ensure the extension tab loads.
    - Close any additional tabs that may have opened during initialization.

3. **Open Extension Settings:**
    - Navigate to `chrome://extensions/`.
    - Access the extensions manager and enable developer mode by interacting with the shadow DOM.

4. **Retrieve Extension ID:**
    - Get the ID of TamperMonkey or ViolentMonkey to interact with its settings directly.

5. **Refresh Extension:**
    - Reload the extension to ensure it’s fully loaded and functional.

6. **Add New User Script:**
    - Navigate to the extension's options page.
    - Load the JavaScript content from a text file.
    - Inject the content into the CodeMirror editor on the options page.

7. **Save and Test the Script:**
    - Save the script using a keyboard shortcut.
    - Open a web page to test the newly added script.

**Conclusion**

By following this guide, you can automate the process of bypassing or solving RecaptchaV2 using Selenium in Python with the help of TamperMonkey or ViolentMonkey. This method can significantly streamline your workflow, allowing you to automate repetitive tasks with ease. Whether you're looking to enhance your web scraping capabilities, automate form submissions, or create custom web interactions, this approach provides a powerful toolset for your automation projects.

Happy automating!
