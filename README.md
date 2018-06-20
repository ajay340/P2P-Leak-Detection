## VPN Torrent Detection
---

This is a small program I created in python to check whether a user is leaking their real IP address while torrenting and being connected to their VPN.

---

** How does it work **

I am using two free web services. 
[CheckMyTorrentIP](http://checkmytorrentip.upcoil.com) is a service that provides an magnet file for a user to download and extracts their IP address.
[WhatIsMyIPAddress](https://whatismyipaddress.com) is a service that does reverse lookups of IP addresses and domains. In addition, the site provides whether a person is using to a VPN or proxy.

First it extract the user's IP address from CheckMyTorrentIP via HTTP request, then it downloads the magnet torrent file in the user's torrent client.
After 15 seconds, CheckMyTorrentIP will extract the IP of the user by looking at the torrent. It then checks that the user's IP extracted from the HTTP request and the IP obtained by the torrent query are the same.
If they are then it checks if the IP is a VPN using WhatIsMyIPAddress. It WhatsIsMyIPAddress says that it has detected that it is an VPN, then a message will display that they are torrenting with their VPN.
If not, then a message will appear saying that they are not torrenting with their VPN.


