commotion-bigboard-gatherer
===========================

A collection of scripts to gather data about nodes on a mesh

In order to save space on nodes (particularly embedded routers), we rely on the OLSR plugin JSONinfo. The gatherer pulls in data from all nodes that its is configured to poll (provided they allow it). This approach allows big-board the option of storing more than just the current status of the mesh, and limits the possible off-mesh connections to a bigboard-server.

The gatherer can write a file locally (file system permissions permitting), or via SSH to a remote bigboard server (NOTE: this feature is incomplete).

Installation/ Configuration
------------

### On the node
Currently the only configuration change on the nodes is a change to "/etc/config/olsrd" look for this block:

    config LoadPlugin
            option library 'olsrd_jsoninfo.so.0.0'
            option accept '0.0.0.0'
            option UUIDFile '/etc/olsrd.d/olsrd.uuid'
        
Change the "accept" option to the IP address of the gatherer.

### On the gatherer
Currently the gatherer has two configuration files.

#### monitored-nodes
The "monitored-nodes" file is currently a simple text file with the IP address per line for each node that is being monitored.

#### bigboard-server-config
The "bigboard-server-config" file is a JSON Formatted file that contains a few settings for how the gatherer should behave. Currently it has three values:

    {
      "bigboard_use_remote_server":false,
      "bigboard_remote_server":"127.0.0.1",
      "bigboard_remote_user":"bigboard",
      "bigboard_nodes_json_path":"."
    }
   
1. bigboard_use_remote_server is a boolean, and is checked so that the gatherer knows what to do with compiled data.
1. bigboard_remote_server is the IP or domain name of the remote bigboard server
1. bigboard_remote_user is the user on the remote machine that will receive the compiled data.
1. bigboard_nodes_json_path is the path __both local and remote__ 


Big Board Server
----------------

The big board server is currently just a clone of [the FreiFunk D3 map](https://github.com/tcatm/ffmap-d3), the gatherer simply supplies the nodes.json file that the map needs to display the nodes.

TODOs
-----
1. Handle remote connections.
