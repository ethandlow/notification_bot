import praw
import webbrowser
import time
from datetime import datetime
import pytz

# Chrome path (replace with your Chrome executable path)
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# Target Reddit user
target_user = 'TARGET_USER'
opened = []

def get_user_info():
    global client_id, client_secret, username, password, user_agent, reddit, target_user
    client_id = input("Client ID: ")
    client_secret = input("Client secret: ")
    username = input("Username: ")
    password = input("Password: ")
    user_agent = input("User agent: ")

    target_user = input("Target username: ")

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         username=username, password=password, user_agent=user_agent)


def utc_to_est(utc_datetime):
    utc_timezone = pytz.timezone('UTC')
    est_timezone = pytz.timezone('US/Eastern')
    utc_datetime = utc_timezone.localize(utc_datetime)
    est_datetime = utc_datetime.astimezone(est_timezone)

    return est_datetime

# Function to check for new posts by the target user
def check_for_new_posts(start_time):
    print(f"Checking for new posts by u/{target_user}...")
    
    # Get the target user's submissions
    user_submissions = reddit.redditor(target_user).submissions.new(limit=1)
    
    for submission in user_submissions:
        id = submission.id
        post_time_utc = datetime.utcfromtimestamp(submission.created_utc)
        post_time_est = utc_to_est(post_time_utc)

        if id not in opened and post_time_utc > start_time:
            print(f"New post by u/{target_user}: {submission.title}")
            print(f"Post created at: {post_time_est.strftime('%Y-%m-%d %H:%M:%S EST')}")
            open_in_chrome(submission.url)
            opened.append(id)

# Function to open a URL in Chrome
def open_in_chrome(url):
    webbrowser.get(chrome_path).open(url)

def run_post_checker():
    start_time = datetime.utcnow()
    print(f"Checking for posts after {start_time}")
    while True:
        check_for_new_posts(start_time)
        
        # Check every 5 minutes (adjust as needed)
        time.sleep(1)

def run_get_post_info(num_posts):
    print(f"Retrieving last {num_posts} from u/{target_user}...")

    user_submissions = reddit.redditor(target_user).submissions.new(limit=num_posts)

    for submission in user_submissions:
        post_time_utc = datetime.utcfromtimestamp(submission.created_utc)
        post_time_est = utc_to_est(post_time_utc)
        print(f"{submission.title} posted at {post_time_est.strftime('%Y-%m-%d %H:%M:%S EST')}")


def main():
    get_user_info()
    while True:
        print("Reddit Bot:\n")
        print("1. Post checker")
        print("2. Get post info")

        user_input = input("Select a feature: ")

        if user_input == "1":
            run_post_checker()
        elif user_input == "2":
            while True:
                num_posts = int(input("Enter number of posts: "))
                if num_posts > 0 and num_posts < 50: break
            run_get_post_info(num_posts)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()