from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_html(link, wait_for_element):
    # Opens browser in background
    opt = Options()
    opt.add_argument("--headless")

    with Edge(options=opt) as browser:
        browser.get("https://yarnsub.com" + link)
        # Waits for element to load if needed
        if wait_for_element:
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "suggestion")))
                return browser.page_source
            except Exception as e:
                return None
        else:
            return browser.page_source


def search(item: str):
    html = get_html("/search?q=" + item.replace(" ", "+"), False)
    soup = BeautifulSoup(html, "lxml")

    # Variable to store potential yarn
    yarn_list = []

    ul_list = soup.find_all(name='ul')[1]

    # Finds list elements containing yarn info
    for li in ul_list.find_all(name='li'):
        if len(yarn_list) == 10:  # Only store the first 10 options
            break

        # Store yarn information (name, brand name, and link) in a dictionary
        brand_name_div = li.find(name='div', attrs={'style': 'font-size: 10pt; letter-spacing: 1px; padding: 2px 0px;'})
        brand_name = brand_name_div.find(name='a', attrs={'style': 'color: #666;'})
        yarn = li.find(name='a', attrs={'style': 'font-size: 15pt;'}, href=True)

        item = {
            "Name": yarn.text,
            "Brand": brand_name.text,
            "Link": yarn['href']
        }
        # Add yarn to list
        yarn_list.append(item)
    return yarn_list


def details(link: str):
    html = get_html(link, True)
    soup = BeautifulSoup(html, "lxml")

    # Dictionary to store all current yarn information
    yarn = {}

    # Stores information
    main_div = soup.findAll(name='div', class_="content")[2]
    yarn["Name"] = main_div.find(name='h1', attrs={'style': 'margin-top: 0px;'}).text.strip()
    yarn["Brand"] = main_div.find(name='div', class_="mainBrand").find('a').text.strip()
    yarn_table = main_div.find(name='table', class_="details")

    for tr in yarn_table.findAll(name='tr'):
        th = tr.find(name='th').text
        if th not in ["Styles:", "Price:"]:  # Ignores style and price
            yarn[th] = tr.find(name='td').text

    # Variable to store substitute yarns
    subs = []

    for sub in soup.find_all(name='div', class_="suggestion"):
        if len(subs) == 5:  # We will only store 5 potential substitutes
            break

        # Store substitute information into dictionary
        item = {}
        name_div = sub.find(name='div', class_="subName")
        item["Name"] = name_div.find(name='a').text.strip()
        item["Match"] = name_div.text.replace("$", "").strip()
        item["Brand"] = sub.find(name='div', class_="subBrand").find(name='a').text.strip()

        msgs = []
        for msg in sub.find_all(name='div', class_="subMsg"):
            msgs.append(msg.find(name='div').text.strip())
        item["Messages"] = msgs

        # Store substitute into list
        subs.append(item)

    return yarn, subs
