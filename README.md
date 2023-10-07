# del_btctalk_posts
Since you cant delete your account on bitcointalk, and deleting posts manually one by one is a pain, i made a python script to automatically delete all posts that can be deleted, and to edit those which can only be edited (changes subject and message to "x")

I couldnt find any terms of service for this website, so not sure if this is even allowed.

# Requirements
Python
Chrome (you can edit the script yourself to change browser if you want)
Selenium installed in python
```pip install selenium```

# How to use
After installing selenium, simply run the python script, it will ask you how many pages of posts your account has (Profile -> Show Posts -> Highest page number available)
just enter the number you see in your profile and then hit enter. It will then open up a chrome browser with the login page for bitcointalk open, you will have 60 seconds to log in and when the 60 seconds are up, the script will start deleting and editing posts from your profile.
Note: When logging in, you should set number of minutes to be logged in to a higher number if you have many posts

# WARNING
This should be obvious, but running this script will try to delete as many of your posts as it can, so dont run it if you dont want that..
