commotion-bigboard-gatherer
===========================

A collection of scripts to gather data about nodes on a mesh

In order to save space on nodes (particularly embedded routers), we rely on the OLSR plugin JSONinfo. The gatherer pulls in data from all nodes that its is configured to poll (provided they allow it). This approach allows big-board the option of storing more than just the current status of the mesh, and limits the possible off-mesh connections to a bigboard-server.

The gatherer can write a file locally (file system permissions permitting), or via SSH to a remote bigboard server (NOTE: this feature is incomplete).

Installation/ Configuration
------------

### On the node
Currently the only configuration change on the nodes is a change to "/etc/config/olsrd" look for a block like:

    config LoadPlugin
            option library 'olsrd_jsoninfo.so.0.0'
            option accept '0.0.0.0'
            option UUIDFile '/etc/olsrd.d/olsrd.uuid'
        
Change the "accept" option to the IP address of the gatherer, or to 0.0.0.0 to allow everyone who can see the node get the OLSR info.

Don't forget to restart OLSR for the change to take effect! If you are SSH'd in to the node, this should work:

    /etc/init.d/olsr restart

### On the gatherer
The gatherer is written assuming Linux with a standard python install.

Currently the gatherer has two configuration files.

#### monitored-nodes
The "monitored-nodes" file is currently a simple text file with the IP address per line for each node that is being monitored.

#### bigboard-server-config
The "bigboard-server-config" file is a JSON Formatted file that contains a few settings for how the gatherer should behave. Currently it has four values:

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

#### Other configurations
If the bigboard gatherer is running on a client that is not itself a node in the mesh, you will need to add some routing information to the gatherer server. Essentially you need to route requests for 5.0.0.0/8 through the wireless AP to keep those addresses from resolving on the wider internet. Assuming you are connected to a node with the IP 103.75.125.1 this command should work:

    ip route add 5.0.0.0/8 via 103.75.125.1

Once that is set up, the last step is to add a cron job for the script, so that the node data gets regularly updated. This example will set it to update every minute.

    * * * * *  /usr/bin/python /home/bigboard/ffhmap/ffmap-node-data.py
    

Big Board Server
----------------

The big board server is currently just a clone of [the FreiFunk D3 map](https://github.com/tcatm/ffmap-d3), the gatherer simply supplies the nodes.json file that the map needs to display the nodes.

Until remote connections are handled, the bigboard_nodes_json_path variable will be used to write the nodes.json file somewhere locally.

TODOs
-----
1. Handle remote connections.
