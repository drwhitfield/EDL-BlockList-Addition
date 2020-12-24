#/usr/bin/python3

'''
Description: Script to add IP addresses and domains to EDL blocklist.

'''

__author__ = 'Donald Whitfield'
__copyright__ = '(c) 2020, Skyline Technologies'
__email__ = 'dwhitfield@skylinenet.net'
__status__ = 'Development Version 3'


import argparse, shutil
import os, time
from datetime import date

parser = argparse.ArgumentParser("blocklist.py")
parser.add_argument('-a', '--add_ip', help="Use to Add An IP Address to Blocklist")
parser.add_argument('-i', '--incident', help="Reference to Service Now Incident Number", required=True)
parser.add_argument('-d', '--domain', help="Use to Add Domain to Blocklist")
parser.add_argument('-c', '--check_list', help="Check That IP or Incident Is Added to Blocklist")

args = parser.parse_args()

ipaddress = args.add_ip
incident = "#" + args.incident
domain = args.domain
today = str(date.today())


blocklistargs, domainlistargs = [],[]
blocklistargs.extend((ipaddress,incident,today))
domainlistargs.extend((domain,incident,today))

print (blocklistargs, domainlistargs)


def main():
    if args.domain is not None:
        domainblock_job()
    elif args.add_ip is not None:
        extipblock_job()

def domainblock_job():
    domainsrc="/var/www/html/DomainBlockList.txt"
    domaindst="/var/www/html/DomainBlockList.txt"+"-"+str(date.today())
    shutil.copy(domainsrc,domaindst)

    with open('/var/www/html/DomainBlockList.txt', 'a+') as filehandle:
        filehandle.write("\n")
        for item in domainlistargs:
            filehandle.write(item + ' ')
        filehandle.close()
    os.system("sed -i '/^$/d' /var/www/html/ExternalBlockList.txt")


def extipblock_job():
    ipsrc="/var/www/html/ExternalBlockList.txt"
    ipdst="/var/www/html/ExternalBlockList.txt"+"-"+str(date.today())
    shutil.copy(ipsrc,ipdst)

    with open('/var/www/html/ExternalBlockList.txt', 'a+') as filehandle:
        filehandle.write("\n")
        for item in blocklistargs:
            filehandle.write(item + ' ')
        filehandle.close()
    os.system("sed -i '/^$/d' /var/www/html/DomainBlockList.txt")


main()

