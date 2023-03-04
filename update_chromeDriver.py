from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Create a new Chrome WebDriver instance
driver = webdriver.Chrome(ChromeDriverManager().install())

# Use the WebDriver as needed
driver.get('https://www.google.com/')