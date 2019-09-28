from twython import Twython

from django.conf import settings


def init_twitter():
    try:
        twitter = Twython(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
        )
    except Exception:
        # Log this error: Authentication Error.
        twitter = None

    return twitter


def send_tweet(context=None):
    twitter = init_twitter()
    if twitter:
        workshop = context.get('workshop', None)
        if workshop:
            try:
                twitter.update_status(status=workshop.get_tweet(context))
            except Exception:
                # Log this error: Status Update error.
                pass
