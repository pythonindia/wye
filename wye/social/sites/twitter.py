from twython import Twython

from wye.social.utils import get_message

def init_twitter(old_function):
    def new_function(context):
        try:
            twitter = Twython(
                settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET,
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET,
            )
        except:
            # Log this error: Authentication Error.
            twitter = None

        old_function(context=context, twitter=twitter)

    return new_function

@init_twitter
def send_tweet(context=None, twitter=None):
    if twitter:
        message = get_message(context)
        print(message)
        try:
            twitter.update_status(status=message)
        except:
            # Log this error: Status Update error.
            pass
    else:
        # Log this error: Authentication Error.
        pass
