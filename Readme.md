### Webscraping with Selenium, a Simple Example
This can be done headless, but for now doing on laptop for rapid development

__Note__: _right click on inspect element and then follow copy menu to get XPATH_

#### requirements.txt
```
selenium>=4.16.0
```

#### Example
```
>>> from selenium import webdriver
>>> driver = webdriver.Chrome()
>>> driver.get('https://put-your-url-here')

>>> print('https://selenium-python.readthedocs.io/locating-elements.html')
https://selenium-python.readthedocs.io/locating-elements.html

>>> input_box = driver.find_element(By.XPATH, "//input[1]")
>>> input_box.send_keys("put_your_code_here")

>>> print('https://iqss.github.io/dss-webscrape/filling-in-web-forms.html')
https://iqss.github.io/dss-webscrape/filling-in-web-forms.html

>>> driver.find_element(By.XPATH, '//button[text()=" Rechercher "]').click()
>>> driver.find_element(By.XPATH, '//button[text()=" Élèves "]').click()

>>> table_body = driver.find_element(By.XPATH, "/html/body/app-root/div/main/div/app-list/div/div[3]/div[1]/table/tbody")
>>> for row in table_body.find_elements(By.XPATH, ".//tr"):
        print([td.text for td in row.find_elements(By.XPATH, ".//td")])

>>> student_list = []
>>> for row in table_body.find_elements(By.XPATH, ".//tr"):
...     l = [td.text for td in row.find_elements(By.XPATH, ".//td")]
...     print(l)
...     if l:
...         student_list.append(l)
...
>>>
>>> len(student_list)
15
>>> next_page_link_click = driver.find.element(By.XPATH, "/html/body/app-root/div/main/div/app-list/div/div[3]/div[2]/nav/ul/li[3]/a/i").click()

```

#### References
* [headless selenium documentation](https://www.selenium.dev/blog/2023/headless-is-going-away/)
Examples for headless and then not headless are below:
```
>>> from selenium import webdriver
>>> options = webdriver.ChromeOptions()
>>> options.add_argument("--headless=new")
>>> driver = webdriver.Chrome(options=options)
>>> driver.get('http://selenium.dev')
>>> driver.quit()
>>>
>>> options.arguments.remove('--headless=new')
>>> driver = webdriver.Chrome(options=options)
>>> driver.get('http://selenium.dev')
>>> driver.quit()
```
* [another example #2](https://www.zenrows.com/blog/headless-browser-python#what-headless-browser-is-included-in-selenium)

<!---
# vim: ai et ts=4 sts=4 sw=4 nu
-->

