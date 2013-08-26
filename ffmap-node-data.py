#!/usr/bin/python
import  os
import  json
import urllib2
import collections

# TODO determine this on the fly or statically set in a more reasonable way
pwd = '/home/bigboard/commotion-bigboard-gatherer/'

# create some sets arrays, etc, for passing data around
ip_mac_map = collections.defaultdict(lambda: None, {})
links = {}
nodes = []

# load the config file
config = json.loads(open(pwd +'bigboard-server-config', 'r').read())

# this function takes decoded json from decode_json() and parses out the node
# data. additionally, this function will build an IP MAC address table.
def parse_node(decoded_json):
    # grab some stuff that we know about the node.

    # TODO this probably shouldn't be hard coded, but we should find out what
    #      the d3 model for multi-radios should be.
    ip4addr = decoded_json['interfaces'][0]['ipv4Address']
    deviceMac = decoded_json['interfaces'][0]['macAddress']
    deviceName = decoded_json['interfaces'][0]['name']

    # this should give us the correct hostname assuming a standard commotion
    host = None
    for i, plugin in enumerate(decoded_json['plugins']):
        if plugin['plugin'] == 'olsrd_nameservice.so.0.3':
            host = plugin['name']



    # for now we are assuming that returned nodes are online, since we're
    # not yet consulting any sort of data store.
    online = True
    # haven't yet figured out how to check clients from the olsr info that
    # makes this a pretty big TODO. 
    client = False
    # eventually we should have a field to enter coordinates, or possibly
    # some sort of Open Street Map geo picker. Until then, this in null.
    geo = None 

    # figure out if this node is a gateway
    gateway = False
    if decoded_json['config']['hasIpv4Gateway'] is True or decoded_json['config']['hasIpv6Gateway'] is True:
        gateway = True 

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
nodespath = '/home/bigboard/ffmap-d3/bigboard-nodes'
for node in os.listdir(nodespath):
    nodefile = open(nodespath +'/'+ node)
    try:
        decoded = json.loads(nodefile.read())
    except (ValueError, KeyError, TypeError):
        decoded = None
    if decoded is not None:
        nodes.append(parse_node(decoded))

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
