import re
import time
import random
import html
import sys

import requests
from bs4 import BeautifulSoup

# TODO: Refactor out into a utility class
def print_error(error_string):
    sys.stderr.write(error_string)

# TODO: Refactor out into a utility class
def print_info(error_string):
    sys.stderr.write(error_string)

class MeetupGroup():
    """
    
    """
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

    def __init__(self, url):
        self.url = url
        self.name = ""
        self.description = ""
        self.events_data = {'meetup_name': '', 'meetup_URL': url, 'events': []}
        self.fetch_events()

    def extract_data_with_default(self, html_content, regex_pattern, default_value):
        try:
            result = re.findall(regex_pattern, html_content)
            if result:
                return result[0]
            else:
                return default_value
        except Exception as e:
            print_error(f"Error: Regex '{regex_pattern}' failed for {self.url} - {e}")
            return default_value

    def fetch_events(self):
        meetup_URL = self.url + "events/"
        try:
            time.sleep(random.randint(1, 4))
            response = requests.get(meetup_URL, headers=self.HEADERS, timeout=10)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:

                soup = BeautifulSoup(response.text, 'html.parser')

                # Get name of Meetup
                meetup_title = soup.find('title')
                if meetup_title:
                    meetup_title_text = meetup_title.text.replace(" | Meetup", "")
                    meetup_title_text = meetup_title.text.replace(" Events", "")
                else:
                    meetup_title_text = "Unknown"
                self.events_data['meetup_name'] = meetup_title_text

                # Get upcoming event area (may need changing for multiple events)
                upcoming_events_elements = soup.findAll("a", {"id" : re.compile('^event-card-e-*')})

                for upcoming_event_element in upcoming_events_elements:
                    upcoming_event = dict()

                    # Pull out event data manually (it's XML and not HTML)
                    try:

                        pattern =  re.compile(r'^<a(.*?)p>', re.DOTALL)
                        matches = re.findall(pattern, str(upcoming_event_element))

                        if matches:
                            # Pull out URL
                            pattern_URL = re.compile(r'href=\"(.*?)\"', re.DOTALL)
                            upcoming_event['URL'] = re.findall(pattern_URL, matches[0])[0]

                            # Pull out event time (parse into readable format)
                            upcoming_event['datetime'] = upcoming_event_element.find("time").text

                            # Pull out event location
                            pattern_location = re.compile(r'<span class=\"text-gray6\">(.*?)</span>', re.DOTALL)
                            upcoming_event['location'] = re.findall(pattern_location, matches[0])[0]

                            # Pull out event title
                            pattern_title = re.compile(r'utils_cardTitle__lbnC_\">(.*?)</span>', re.DOTALL)
                            upcoming_event['title'] = html.unescape(re.findall(pattern_title, matches[0])[0].strip())

                            # Pull out event description
                            pattern_description = re.compile(r'<p class="mb-4">(.*?)</')
                            default_description = "No description found."
                            upcoming_event['description'] = self.extract_data_with_default(matches[0], pattern_description, default_description)
                            upcoming_event['description'] = html.unescape(upcoming_event['description'].strip())

                    except Exception as e:
                        print_error(f"Error occured retrieving event information: {e}")

                    # Add this event to events array
                    self.events_data['events'].append(upcoming_event)

                return self.events_data

            else:
                print_error(f"Failed to retrieve the page. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print_error(f"An error occurred: {e}")

    def get_events(self):
        return self.events_data
    
    def get_just_events(self):
        return self.events_data['events']

    def print_events(self):
        print("Events for", self.events_data['meetup_name'])
        for event in self.events_data['events']:
            print("  Event title:",event['title'])
            print("  Event URL:",event['URL'])
            print("  Event time:",event['datetime'])
            print("  Event location:",event['location'])
            print()

    def print_events_summary(self):
        events_found = len(self.events_data['events'])
        if events_found == 1:
            print_info(f"1 event found for {self.events_data['meetup_name']}\n")
        else:
            print_info(f"{events_found} events found for {self.events_data['meetup_name']}\n")
    
    def get_name(self):
        return self.name

    def __str__(self):
        return str(self.url)