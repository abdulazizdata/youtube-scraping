from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import requests

urls = [
    'AlexGyverShow'
]


def main():
    for url in urls:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.maximize_window()
        driver.get('https://www.youtube.com/c/{}/videos?view=0&sort=p&flow=grid'.format(url))

        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time

            # Break the loop when the height we need to scroll to is larger than the total scroll height

            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, 'lxml')
            titles = soup.findAll('a', id='video-title')

            for title in titles:
                driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                time.sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")

            if (screen_height) * i > scroll_height:
                break

        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        titles = soup.findAll('a', id='video-title')
        # for title in titles:
        #     print(title.text)
        views = soup.findAll('span', class_='style-scope ytd-grid-video-renderer')
        # for view in views:
        #     print(view.text)
        video_urls = soup.findAll('a', id='video-title')
        print(f'Channel: https://www.youtube.com/{url}')
        a = 0  # views and time
        j = 0  # urls
        for title in titles:
            # print(title.text)
            req = requests.get("https://www.youtube.com" + video_urls[j].get("href"))
            so = BeautifulSoup(req.content, 'lxml')
            likes = so.find('yt-formatted-string', class_='style-scope ytd-toggle-button-renderer style-text')

            print(f'\n{title.text}\t{views[a].text}\thttps://www.youtube.com{video_urls[j].get("href")}\tlikes: {likes}')

            a += 2
            j += 1


main()
