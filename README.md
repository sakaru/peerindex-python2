# PeerIndex Python2 API Client

The PeerIndex API allows you to tie the functionality of PeerIndex to your own application.

## Usage

Get an API key from here: http://developers.peerindex.com/

See examply.py for some sample usage, but essentially:
```python
api = peerindex.PeerIndex('f183qza9k88mjynhtjfc56ce')
query = {'twitter_screen_name' : 'fhuszar'}
basic = api.ActorBasic(query)
```

