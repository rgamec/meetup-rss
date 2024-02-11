#! /opt/homebrew/bin/python3
import sys

from MeetupGroup import MeetupGroup
from ConfigLoader import ConfigLoader
from FeedBuilder import FeedBuilder

'''
TODO: Pull out attendee counts per event
TODO: Pull out event description per event
TODO: Sort out STDIN/config file logic
TODO: Sort out config file location login
TODO: Make sure information gets output via STDERR (vs STDOUT)
TODO: Add error-handling to regex searches
TODO: Add error-handling to URL parsing
TODO: Add usage/version info
TODO: Add switch for rolling all the feeds into one file
TODO: Add switch for defining optional file output
'''

# TODO: Refactor out into a utility class
def print_error(error_string):
    sys.stderr.write(error_string)

# TODO: Refactor out into a utility class
def print_info(error_string):
    sys.stderr.write(error_string)

# Attempt to first load a config file — otherwise read in group URLs from STDIN
group_URLs = []

# Groups passed in via STDIN take precedence over user config
if not sys.stdin.isatty():
    for stdin_line in sys.stdin:
        if 'Exit' == stdin_line.rstrip():
            break
        group_URLs.append(stdin_line)

try:
    config = ConfigLoader()
    group_URLs.extend(config.get_config())
except (FileNotFoundError) as e:
    print_error(f"Unable to find an existing configuration")
except Exception as e:
    print_error(f"General error in loading config encountered")

if len(group_URLs) == 0:
    print_error("Error: No Meetup group URLs provided. Either set them in .meetup-rss.conf or pass them in via STDIN.")
    sys.exit(1)

# For each group retrieve the list of upcoming events
COMBINE_FEEDS = True
combined_events = []

for group_URL in group_URLs:
    meetup_group = MeetupGroup(group_URL)
    # meetup_group.print_events()
    meetup_group.print_events_summary()

    # Pass the data structure of event data into FeedBuilder
    feed_builder = FeedBuilder(meetup_group.get_events())

    if COMBINE_FEEDS:
        # this
        combined_events.extend(meetup_group.get_just_events())
    else:
        # this
        # Print to STDOUT by default, otherwise set file path with -o
        feed_builder.save_feed()

if COMBINE_FEEDS:
    # Define the RSS feed header properties
    combined_event_complete = {'meetup_URL': 'http://meetup.com', 'meetup_name': 'Meetup Upcoming Events'}

    # Add on all discovered upcoming events and print feed XML to STDOUT
    combined_event_complete['events'] = combined_events
    combined_feed_builder = FeedBuilder(combined_event_complete)
    print(combined_feed_builder.get_feed())