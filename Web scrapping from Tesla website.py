#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install selenium')


# In[12]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd


# In[13]:


options = Options()
options.headless = True
# options.add_argument("--headless")
# options.add_argument('window-size=1920x1080')
web = "https://www.tesla.com/en_US/findus/list/stores/United%20States"


# In[14]:


driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(web)


# In[17]:


states = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="state"]')))
stt = []
location = []
stree = []
city = []
postal = []
store = []
roads = []
services = []
demo_link = []
for state in states:
    vcards = WebDriverWait(state, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, './/address[contains(@class,"vcard")]')))
    for card in vcards:
        state_name = state.find_element(By.TAG_NAME, 'h2').text
        location_name = card.find_element(By.CLASS_NAME, 'anchor-container').text
        street = card.find_element(By.XPATH, '//span[@class="street-address-states"]').text

        locality = card.find_element(By.CLASS_NAME, 'locality-city-postal').text
        parts = locality.split(',')

        city_nma = parts[0].strip()
        state_postal_parts = parts[1].strip().split()
        post_code = state_postal_parts[0] + "" + state_postal_parts[1]

        store_name = card.find_element(By.XPATH, '//span[@class="tel"]/span[contains(@class, "value")][1]').text
        road_asst = card.find_element(By.XPATH, '//span[@class="tel"]/span[contains(@class, "value")][2]').text
        service = card.find_element(By.XPATH, '//span[@class="tel"]/span[contains(@class, "value")][3]').text
        demo = card.find_element(By.XPATH, '//a[contains(@class,"demo-drive-link")]').get_attribute('href')
        stt.append(state_name)
        location.append(location_name)
        stree.append(street)
        city.append(city_nma)
        postal.append(post_code)
        store.append(store_name)
        roads.append(road_asst)
        services.append(service)
        demo_link.append(demo)


# In[18]:


driver.quit()
df_stores = pd.DataFrame(
    {'State': stt, 'Location Name': location, 'Street Address': stree, 'City': city, 'Postal': postal, 'Store': store,
     'Roadside Assistance': roads, 'Service': services, 'Demo Link': demo_link})
df_stores.to_csv('tesla_stores.csv', index=False)
print(df_stores)


# In[19]:


df_stores


# In[ ]:




