import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from instapy import InstaPy
from instapy.util import smart_run


class InstagramBot():
    #Users already followed
    prev_user_list = []      
    chromedriver_path = 'C:/webdriver/chromedriver.exe'
    
    def __init__(self,username,password):

        """Details the bot will use to log in to your instagram account."""

        #Ensure the browser Uses English as the default language
        self.browserprofile = webdriver.ChromeOptions()
        self.browserprofile.add_experimental_option('prefs',{'intl.accept_languages': 'en,en_US'})

        self.browser = webdriver.Chrome(executable_path=InstagramBot.chromedriver_path)
        self.username = username
        self.password = password

        #To store the new details
        self.new_followed = []
        self.followed = 0
        self.liked = 0
    
    def login(self):
        # To log in the bot, sleep is used to create delays so that the bot's actions can seem normal.

        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

        username = self.browser.find_element_by_name('username')
        username.send_keys(self.username)
        password = self.browser.find_element_by_name('password')
        sleep(5)
        password.send_keys(self.password)
        sleep(2)
        password.send_keys(Keys.ENTER)
        sleep(4)
    
    def follow(self):
        
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            sleep(2)
        else:
            pass


    def unfollowWithUsername(self,username):

        self.browser.get('https://www.instagram.com/' + username + '/')
        sleep(randint(1,4))

        followButton = self.browser.find_element_by_css_selector('#react-root > section > main > div > header > section > div.Y2E37 > a > button')

        #If you follow the user but they don't follow you back, unfollow
        if(followButton.text == 'Following'):
            followButton.click()
            sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")
            #Maybe you could invoke the follow function here
            #There is also the possibility of creating downloading all your data from instagram then comparing with your list of followers
    def likePicture(self):
        #Liking the picture
            button_like = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

            button_like.click()
            sleep(randint(5,12))

    def followByHashtag(self):
        sleep(5)
        hashtag_list = ['writers','bookstagram','africawrites']

        for hashtag in hashtag_list:

            self.browser.get('https://www.instagram.com/explore/tags/' + hashtag_list[randint(0,len(hashtag_list))] + '/')
            sleep(5)

            first_thumbnail = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')

            first_thumbnail.click()
            sleep(randint(1,3))

            try:
                for x in range(1,200):
                    # Get the username of the account on the first thumbnail
                    username = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text

                    if username not in self.prev_user_list:
                        # If we had not already followed the user
                        if self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                            # Follow the person
                            self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                            sleep(5)
                            self.new_followed.append(username)
                            self.followed +=1

                            #Liking the picture
                            button_like = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

                            button_like.click()
                            self.liked +=1
                            sleep(5)

                            #Tracking the Bot
                            print(f'{hashtag},{x}')

                    self.browser.find_element_by_link_text('Next').click()
                    sleep(5)

            # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
            except:
                continue

            self.output()

    def followAndLikeByLocation(self):
        #Using Instapy to follow likers of photos
        session = InstaPy(username=self.username,
                  password=self.password,
                  headless_browser=False)
        
        with smart_run(session):
            """ Activity flow """               
            session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=True,
                                    max_followers=4590,
                                    min_followers=45,
                                    min_following=77)

            
            session.set_user_interact(amount=5,
				 percentage=70,
                  randomize=True,
                   media='Photo')
            # session.set_do_like(enabled=False, percentage=70)
            session.set_do_follow(enabled=True, percentage=70)
           
            session.set_do_comment(enabled=False, percentage=50)

            session.like_by_locations(['235483975/kenyatta-university/'],amount=1000)

      
    def output(self):
        #People we have followed so far           
        
        for i in range(0,len(self.new_followed)):
            self.prev_user_list.append(self.new_followed[i])

        updated_user_df = pd.DataFrame(self.prev_user_list)
        updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
        print('Liked {} photos.'.format(self.liked))
        print('Followed {} new people.'.format(self.followed))

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()



bot = InstagramBot('ebookshopke', 'walterSTRIDER007')
bot.followAndLikeByLocation()

        
