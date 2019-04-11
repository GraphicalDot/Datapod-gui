

from InstagramAPI import InstagramAPI
import time



def instagram_login(username, password):
    print (f"Instagram username {username}")
    print (f"Instagram password {password}")
    instagram_object = InstagramAPI(username, password)
    print (f"Instagram object {instagram_object}")
    
    status = instagram_object.login()
    
    print (status)
    if not status:
        raise Exception()
    return instagram_object


def get_all_posts(instagram_object, myposts=[]):
    has_more_posts = True
    max_id=""

    while has_more_posts:
        instagram_object.getSelfUserFeed(maxid=max_id)
        if instagram_object.LastJson['more_available'] is not True:
            has_more_posts = False #stop condition
            print ("stopped")
        
        max_id = instagram_object.LastJson.get('next_max_id','')
        myposts.extend(instagram_object.LastJson['items']) #merge lists
        time.sleep(2) # Slows the script down to avoid flooding the servers 
    
    return max_id, myposts 