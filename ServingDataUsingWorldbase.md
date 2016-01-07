# Introduction #

Using worldbase to store your resources is especially convenient when attempting to access them remotely through a server, as the unique handles assigned to the data when registered in worldbase ensure ease of access. The server used here is an XML-RPC server, a server that encodes the data using XML (Extensible Markup Language) and then HTTP as the data transport method. Creating an XML-RPC server is very simple, and will allow the user to retrieve databases stored in worldbase, even from independent computers.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# A Helpful Example #

Import worldbase from pygr, then reference the worldbase resource you wish to serve. In this case, the reference is worldbase.Bio.Seq.Genome.ECOLI.ecoli. A NLMSA is a data structure used to store the genome/sequence maps. The alignment and sequence databases stored in the NLMSA can currently be accessed by worldbase.

Next, the server is assigned a name; this name will be used a layer name within worldbase, as well as a port number. The port number can be set to any number that is currently available. Finally, the server can be accessed easily by the URL from any location, as long as the URL is set to the WORLDBASEPATH. The default WORLDBASEPATH is http://biodb2.bioinformatics.ucla.edu:5000, and thus if this remains unchanged, the user will not be able to add or delete resources to/from worldbase. Furthermore, the server must be assigned a name (like 'rachel') that will also be used as the layer name for the worldbase resource when attempting to access it remotely.

In order to access the newly-created server from a remote location, the server must be set as the WORLDBASEPATH. WORLDBASEPATH searches for worldbase resources in three steps: 1) in the current directory; 2) in the home directory; and 3) from the XMLRPC server. It is essential to assign the server as to WORLDBASEPATH, or an error will result. The correct address to give to WORLDBASEPATH would be the URL of your server (http://somehost:1215), with somehost as the server address. Firewalls may be present, and could potentially prevent access to the XML-RPC server, and thus should be addressed as need be.

```
from pygr import worldbase
nlmsa = worldbase.Bio.Seq.Genome.ECOLI.ecoli() 
server = worldbase.getResource.newServer('rachel', withIndex=True, port=1215)
server.serve_forever()
```