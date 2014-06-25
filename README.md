[![alt tag](http://img.shields.io/badge/maintainer-natmey-yellow.svg)](https://github.com/natmey)
commotion-bigboard-gatherer
===========================

A collection of scripts to compile data about nodes on a mesh

In order to save space on nodes (particularly embedded routers), we rely on the OLSR plugin JSONinfo, curl and simple shell scripts. The listener takes data from nodes, and writes a file with their JSONinfo. The gatherer in turn takes that data from all nodes and compiles it into a format that the D3 visualizer can read. This approach allows big-board the option of storing more than just the current status of the mesh, and will eventually support multiple Commotion mesh networks.

The gatherer can write a file locally (file system permissions permitting), or via SSH to a remote bigboard server (NOTE: this feature is incomplete).

Installation/ Configuration
------------

### On the node
The nodes should have a configuration page in the Commotion menu. This should modify the `/etc/config/commotion-dash` file. The file looks something like:

    config dashboard
            option gatherer '103.75.125.142'
            option enabled 'true'
                
                
These configurations are read by the `commotion-bigboard-send` script (`/usr/bin/commotion-bigboard-send`), which sends that information to the gaterer.

Until the packaging is complete, you will need to install curl. This command should do it:

    opkg update; opkg install curl
    
### On the gatherer
The gatherer is written assuming Linux with a standard python install, and a web server that allows the execution of python scripts.

The gatherer keeps its configuration in a json file

#### bigboard-server-config
The "bigboard-server-config" file is a JSON Formatted file that contains a few settings for how the gatherer should behave. Currently it has four values:

    {
      "bigboard_debug":false,
      "bigboard_use_remote_server":false,
      "bigboard_remote_server":"127.0.0.1",
      "bigboard_remote_user":"bigboard",
      "bigboard_nodes_json_path":"."
    }
   
1. bigboard_debug is a development flag used at times to make the script behave differently during development. Will probably be replaced by verbosity at some point. This should probably just be left as false.
1. bigboard_use_remote_server is a boolean, and is checked so that the gatherer knows what to do with compiled data.
1. bigboard_remote_server is the IP or domain name of the remote bigboard server
1. bigboard_remote_user is the user on the remote machine that will receive the compiled data.
1. bigboard_nodes_json_path is the path __both local and remote__ 

#### Other configurations
The last step is to add a cron job for the script, so that the node data gets regularly updated. This example will set it to update every minute.

    * * * * *  /usr/bin/python /home/bigboard/ffhmap/ffmap-node-data.py
    

Big Board Server
----------------

[The big board server](https://github.com/opentechinstitute/ffmap-d3) is currently a modified clone of [the FreiFunk D3 map](https://github.com/tcatm/ffmap-d3), the listener and the gatherer supply the nodes.json file that the map needs to display the nodes.

Until remote connections are handled, the bigboard_nodes_json_path variable will be used to write the nodes.json file somewhere locally.

TODOs
-----
1. Handle remote connections.
