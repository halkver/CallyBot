from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
import re
from collections import OrderedDict


def scrape(username, password):
    """Scrapes Blackboard. Returns a list of lists [assignment_name, cource_code, course_name, due_date]"""
    driver = webdriver.Chrome()
    # Log in via Feide
    driver.get("https://adfs.ntnu.no/adfs/ls/?wa=wsignin1.0&wtrealm=urn%3afederation%3aMicrosoftOnline&wctx=estsre"
               "direct%3d2%26estsrequest%3drQIIAa1QPWsUQQDN3uUKQ4RgbRkLkbnZ2Z2P3YEgFzi0iMmZg5zaHPN1ZpPbmXVn94z-"
               "BsGPPyCkTGEhVldapgipUwYCVgpWksrN_QArq8d7j_d4vJUlfne_qgrPIbSVrbtyKtShdKLUXeVyWN5ZWfvQHp28r_XOx-vj5"
               "_P0YHASDP4VeW2kKAoPpVTAi3wKvHdgc3Or39vdho0Dc6frqYGirvahctbXufke3BvTBOFUUQqaoAGYxRSkaUwA0pgKTFiCE3"
               "YeBD-C4KLVGTbF0WVrdYGDkZFD765bpC4td8JnnluRG88rxYe9J1scddFCyTSYuDIXFa-tL4zKJpnRn9q3b3ZGRXcB4df2epg"
               "KFFIWgSSKJgBjyoAgUgAiZcxISpkKyby9jilipKEgThgDWIQhEJQowBRiWkYiwaE8X179sxwcd5ojn5LfXz6_2-t_O_t1tZT-vH"
               "_agbPR0L44eqWrlwdsBxm6Hc9mhw4dkQf4cflsYo2ytBfZN4_e9jcijua39P--_uENGZRulmlTboxRSMboLw2")
    driver.find_element_by_xpath("//select[@name='org']/option[text()='NTNU']").click()
    driver.find_element_by_name("submit").click()
    username_field = driver.find_element_by_name("feidename")
    username_field.send_keys(username)
    password_field = driver.find_element_by_name("password")
    password_field.send_keys(password)
    password_field.submit()
    # Login complete
    wait = ui.WebDriverWait(driver, 3)  # Wait duration before throw exception, needed to load entire HTML
    try:
        wait.until(lambda driver: driver.find_element_by_id('quick_links_wrap'))  # Wait for the site to load properly
    except TimeoutException:
        driver.quit()
        return "error"

    driver.get(
        "https://ntnu.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_65_1")  # Go to course list
    try:
        wait.until(lambda driver: driver.find_element_by_id(
            'block::1-dueView::1-dueView_1'))  # Wait for the site to load properly
    except TimeoutException:
        driver.quit()
        return "error"

    html = driver.execute_script("return document.documentElement.innerHTML;")  # Get element HTML for assignments
    listing = re.findall('<li id="1-dueView::.*?"><span>.*?  <a id="nmenu::.*?" class="cmimg editmode" href="#menuDiv"'
                         ' title="(.*?) Alternativer"><img id="cmimg_nmenu::.*?" src="https://ntnu.blackboard.com/'
                         'images/ci/icons/cm_arrow.gif" alt=".*?"></a> <div class="course"><a target=".*?" href=".*?">'
                         '(.*?) (.*?) \(.*?\)</a><span class="due"> - Leveringsfrist (.*?)</span></div></span></li>',
                         html)  # Regex to filter out only relevant data.
    # (.*?) is for fetched data, .*? for irrelevant. Don't touch unless you want to read up on regex.
    driver.quit()  # Closing the browser
    listing = list(
        OrderedDict.fromkeys(listing))  # Removes duplicates, because blackboard loves to create more work than needed
    return listing  # In format list of (assignment_name, cource_code, course_name, due_date)
