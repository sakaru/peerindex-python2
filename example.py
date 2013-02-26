#!/usr/bin/env python2
import ConfigParser
import peerindex

# Read the API key from the config file
config = ConfigParser.RawConfigParser()
flag = config.read('peerindex.settings.cfg')
if not flag:
    raise Exception("Config file needs to be created, please read the readme.")


def display(basic, extended, topics):
    benchmarkTopicsText = ""
    for benchmarkTopic in topics['benchmark_topics']:
        benchmarkTopicsText += "\t" + benchmarkTopic['name'] + "\n"
    topicsText = ""
    for topic in topics['topics'][0:5]:
        topicsText += "\t" + topic['name'] + "\n"
    influencesText = ""
    message = """
Name:      {name}
PeerIndex: {peerindex}
GeoName location ID: {location}
Topics:
{topicsText}
Benchmark Topics:
{benchmarkTopicsText}

"""
    print message.format(name = basic['twitter']['name'],
                         peerindex = basic['peerindex'],
                         location = extended['demographics']['location']['geoname_id'],
                         topicsText = topicsText,
                         benchmarkTopicsText = benchmarkTopicsText)



# Instantiate the API
api = peerindex.PeerIndex(config.get('api', 'key'))

# Get the profile to query
name = raw_input("Enter a username [fhuszar]: ")
if not name:
    name = "fhuszar"

# Query the profile
query = {'twitter_screen_name' : name}
try:
    basic    = api.actorBasic(query)
    extended = api.actorExtended(query)
    topics   = api.actorTopic(query)
    display(basic, extended, topics)

except peerindex.PeerIndexError as err:
    print "ERROR: check your API key"
except ValueError as err:
    print "ERROR: check your API key"
