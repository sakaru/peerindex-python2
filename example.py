#!/usr/bin/env python2
import ConfigParser
import peerindex

# Read the API key from the config file
config = ConfigParser.RawConfigParser()
flag = config.read('peerindex.settings.cfg')
if not flag:
    raise Exception("Config file needs to be created, please read the readme.")


def display(basic, extended, topics, graph):
    benchmarkTopicsList = []
    for benchmarkTopic in topics['benchmark_topics']:
        benchmarkTopicsList.append(benchmarkTopic['name'])
    benchmarkTopicsText = "\n\t".join(benchmarkTopicsList)
    topicsList = []
    for topic in topics['topics'][0:5]:
        topicsList.append(topic['name'])
    topicsText = "\n\t".join(topicsList)
    influencesList = []
    for influences in graph['influences'][0:5]:
        influencesList.append(influences['peerindex_id'])
    influencesText = "\n\t".join(influencesList)
    message = """
Name:      {name}
PeerIndex: {peerindex}
GeoName location ID: {location}
Topics: {topicsText}
        ...
Benchmark Topics: {benchmarkTopicsText}
        ...
Influences: {influencesText}
        ...
"""
    print message.format(name = basic['twitter']['name'],
                         peerindex = basic['peerindex'],
                         location = extended['demographics']['location']['geoname_id'],
                         topicsText = topicsText,
                         benchmarkTopicsText = benchmarkTopicsText,
                         influencesText = influencesText)



# Instantiate the API
api = peerindex.PeerIndex(config.get('api', 'key'))

# Get the profile to query
name = raw_input("Enter a username [mischatuffield]: ")
if not name:
    name = "mischatuffield"

# Query the profile
query = {'twitter_screen_name' : name}
try:
    basic    = api.actorBasic(query)
    extended = api.actorExtended(query)
    topics   = api.actorTopic(query)
    graph   = api.actorGraph(query)
    display(basic, extended, topics, graph)

except peerindex.PeerIndexError as err:
    print "ERROR: check your API key"
except ValueError as err:
    print "ERROR: check your API key"
