#!/usr/bin/python
import  os
import  json
import urllib2
import collections

# TODO determine this on the fly or statically set in a more reasonable way
pwd = '/home/bigboard/ffhmap/'
ip_mac_map = collections.defaultdict(lambda: None, {})
links = {}
nodes = []

config = json.loads(open(pwd +'bigboard-server-config', 'r').read())

# this function takes a url of the json file, and returns a decoded json obj
def decode_json(url):
    try: 
        ret = json.loads(urllib2.urlopen(url).read())
        return ret
    except (ValueError, KeyError, TypeError):
        return "JSON format error"

# this function takes decoded json from decode_json() and parses out the node
# data. additionally, this function will build an IP MAC address table.
def parse_node(decoded_json):
    # grab some stuff that we know about the node.
    ip4addr = decoded_json['interfaces'][0]['ipv4Address']
    deviceMac = decoded_json['interfaces'][0]['macAddress']
    deviceName = decoded_json['interfaces'][0]['name']
    host = decoded_json['config']['olsrdBuildHost']
    # set the gateway value
    gateway = True
    online = True
    client = True
    geo = None 
    if decoded_json['config']['hasIpv4Gateway'] is False and decoded_json['config']['hasIpv6Gateway'] is False:
        gateway = False       

        # pass some data to sets outside the function


    ip_mac_map[ip4addr] = {'mac':deviceMac}
    node_links = decoded_json['links']
    links[deviceMac] = node_links

        # return the ffhmap formatted data
    return {'id' : deviceMac, 'name' : host, 'flags' : {'client' : client, 'online' : online, 'gateway' : gateway }, 'geo' : geo}

# this loop will pull the node info, and build a set with all of relevant info;
# since ffhmap wants MAC addresses, and OLSR info deals in IP addresses, we 
# will have to map those pieces of data, and build link information only after
# we have gone through all the nodes, and recorded their mac addresses.
for ip in open(pwd +'monitored-nodes', 'r').readlines():
    url = 'http://'+ip+':9090/all'
    nodes.append(parse_node(decode_json(url)))

# d3 actually needs consistent indexing so we need to add that to our map
for i, node_data in enumerate(nodes):
    for ipv4 in ip_mac_map:
        if ip_mac_map[ipv4]['mac'] == node_data['id']:
            ip_mac_map[ipv4]['index'] = i

# with the the complete set of IP to MAC mapping we can now figure out the
# right mapping
out_links = []
for linkID in links:
    for link in links[linkID]:
        target = None
        source = None
        destIP = str(link['remoteIP'])
        if ip_mac_map[destIP] is not None:
            target = ip_mac_map[destIP]['index']

        localIP = link['localIP']
        if ip_mac_map[localIP] is not None:
            source = ip_mac_map[localIP]['index']

        if source is not None and target is not None:
            destMac = ip_mac_map[destIP]['mac']
            localMac = ip_mac_map[localIP]['mac']
            localIP = links[linkID][0]['localIP']
            linksID = str(localMac)+'-'+ str(destMac)
            local_quality = links[linkID][0]['linkQuality']
            neighbor_quality = links[linkID][0]['neighborLinkQuality']
            quality = str(local_quality) +', '+ str(neighbor_quality)
            out_links.append({'id' : linksID, 'source' : source, 'quality' : quality, 'target': target})

if config['bigboard_use_remote_server'] == False and config['bigboard_debug'] == False:
    json_out = {'nodes':nodes, 'links':out_links}
    with open(config['bigboard_nodes_json_path']+'/nodes.json', 'w') as outfile:
        json.dump(json_out, outfile)
