import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


print("Starting Driver")
driver = Driver(uc=True,extension_dir="extensions/Tampermonkey") # Replace your extension directory here
driver.maximize_window()

# wait for Extension tab to close
time.sleep(4)

while True:
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    else:
        driver.switch_to.window(driver.window_handles[-1])
        break
# open extension settings
driver.uc_open("chrome://extensions/")

# Clicking Dev Mode to True
wait = WebDriverWait(driver, 10)
extensions_manager = wait.until(EC.presence_of_element_located((By.TAG_NAME, "extensions-manager")))

shadow_root1 = driver.execute_script("return arguments[0].shadowRoot", extensions_manager)

shadow_root2= shadow_root1.find_element(By.CSS_SELECTOR, '#toolbar')
shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", shadow_root2)

shadow_root3 = shadow_root2.find_element(By.CSS_SELECTOR, '#devMode')
shadow_root3.click()

# Getting Extension ID
view_manager = shadow_root1.find_element(By.ID, "items-list")

shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", view_manager)

extensions = shadow_root2.find_element(By.CSS_SELECTOR,"#extensions-section > div")

all_extensions = extensions.find_elements(By.XPATH,".//*")

extension_id = all_extensions[0].get_attribute("id")

# Refreshing the extension
shadow_root4 = driver.execute_script("return arguments[0].shadowRoot", all_extensions[0])
reload_extension = shadow_root4.find_element(By.CSS_SELECTOR,"#dev-reload-button")
reload_extension.click()

time.sleep(2)
if len(driver.window_handles)>1:
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
else:
    driver.switch_to.window(driver.window_handles[0])


# Visiting Extension Options
driver.uc_open(f"chrome-extension://{extension_id}/options.html#nav=new-user-script+editor")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".CodeMirror"))
)

# Getting the Script to Upload
with open("Recaptcha.txt", "r", encoding="utf-8") as file: # Here You Replace Recaptcha.txt to your script in text file (if you have JS file then copy the content to txt file and then use)
    new_text = file.read()

driver.execute_script("""
    var editor = document.querySelector('.CodeMirror').CodeMirror;
    editor.setValue(arguments[0]);
    editor.refresh();
""", new_text)

time.sleep(1)

# Saving The Script 
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()

# Testing The Script
driver.uc_open("https://www.google.com/recaptcha/api2/demo")
