#Created by Ajay Shah
#Description: Automated program, while torrenting, determines if one's IP address is leaking when connected to a VPN

from bs4 import BeautifulSoup
import requests
import random
import string
import hashlib
import webbrowser
import time


with requests.Session() as c:
    m = hashlib.sha1()
    get_url = 'http://checkmytorrentip.upcoil.com/?hash=' #uses this site to extract IP when torrenting

    #creating a sha1 hash value to for the torrent service to take and create a magnet file out of
    random_val = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(40)])
    encode_val = random_val.encode('utf-8')
    updated_val = m.update(encode_val)
    hash_val = m.hexdigest()
    url = get_url.__add__(hash_val)

    magent_first = 'magnet:?xt=urn:btih:'
    magnet_middle = magent_first.__add__(hash_val)
    magnet_last = magnet_middle.__add__('&dn=CheckMyTorrentIPAddress+Tracking+Link&tr=http%3A%2F%2Fcheckmytorrentip.upcoil.com%2F')
    magnet_url = magnet_last

    print('For debugging: ', url)

    vpn_check = 'https://whatismyipaddress.com/proxy-check' #uses this site to tell if your IP is a VPN

    #Grabbing the information if it an VPN
    try:
        vpn_check_url = c.get(vpn_check)
        check_vpn_soup = BeautifulSoup(vpn_check_url.text, 'html.parser')
        vpn_tag = check_vpn_soup.find('p')
        vpn_value = check_vpn_soup.select('p[style]')[1]

    except requests.exceptions.ConnectionError:
        print("\nCould not connect to the internet, please check your connection and try again.")

    else:

        is_proxy_str = str(vpn_value)
        proxy_textsoup = BeautifulSoup(is_proxy_str, 'html.parser')
        is_proxy = str(proxy_textsoup.text)

        proxy_working = 'Proxy server detected.'


        #Getting IP Address while just connecting to the internet
        connection_ip = c.get(url)
        soup = BeautifulSoup(connection_ip.text, 'lxml')
        tag = soup.find('span')
        user_ip = soup.select('span[id="remote-ip"]')[0]

        obtaining_ip = str(user_ip)
        newsoup = BeautifulSoup(obtaining_ip, 'lxml')

        ip_address = newsoup.text

        print('Your IP Address is: ', ip_address)
        print('Opening up your torrent client...')
        print('Please download the file, it will obtain your IP while torrenting. (It will not actually download anything)')
        time.sleep(5)
        webbrowser.open(magnet_url)

        print('Waiting 15 seconds to extract IP while torrenting...')
        time.sleep(15)

        #Getting IP Address while torrenting
        try:
            connection2_ip = c.get(url)
            thirdsoup = BeautifulSoup(connection2_ip.text, 'lxml')
            tag2 = thirdsoup.find('td')
            tag3 = thirdsoup.select('td')[1]

        except:
            print("\nThere was an error extracting the IP of your torrent, please check that your torrent application can reach the internet and try again.")

        else:
            compared_ip = str(tag3)

            extract_torrent_ip = BeautifulSoup(compared_ip, 'lxml')

            torrent_ip = extract_torrent_ip.text


            print("Your IP address while torrenting is: ", torrent_ip)
            print('\n')

            #Determining if you are connected to the VPN while torrenting
            if proxy_working == is_proxy:
                if ip_address == torrent_ip:
                    print("You are torrenting with your VPN.\n")
                else:
                    print("You are connected to your VPN but not using the same IP for torrentings.\n")

            else:
                print("You are NOT using your VPN to torrent.\n")
