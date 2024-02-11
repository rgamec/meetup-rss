from datetime import datetime
import rfeed

class FeedBuilder():
    """_summary_
    """

    def __init__(self, feed_contents) -> None:
        self.feed_content = feed_contents

        # Set title of RSS feed
        title = feed_contents['meetup_name']

        # Set description of RSS feed
        description="Upcoming Events"

        # Set URL for Meetup group
        link = feed_contents['meetup_URL']

        # Set language of RSS feed
        language="en-US"

        self.feed = rfeed.Feed(title=title,
        description=description,
        language=language,
        items=self.build_events_array(),
        link=link)

    def parse_date(self, date):

        # The format of the date string
        date_format = "%a, %b %d, %Y, %I:%M %p %Z"

        # Parse the string into a datetime object
        return datetime.strptime(date, date_format)
    
    def build_events_array(self):
        items = []
        for event in self.feed_content['events']:

            # Parse date into something we can handle
            pubDate = self.parse_date(event['datetime'])

            # Build the feed item text (from description + location)
            event_description = f"Description: {event['description']}&lt;br&gt;Location: {event['location']}"

            item = rfeed.Item(
                link = event['URL'],
                description = event_description,
                title = event['title'],
                pubDate = pubDate,
                guid = rfeed.Guid(event['URL'])
            )
            
            items.append(item)
        return items

    def get_feed(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.feed.rss()
    
    def save_feed(self):
        print(self.get_feed())
        return "done"