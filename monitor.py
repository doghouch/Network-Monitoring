#!/usr/bin/python3

import sys
import time
import os.path

STATS_DIR = "/sys/class/net"

def check_adapter():
	"""
		Process arguments
	"""
	if len(sys.argv) == 1:
		print("ERROR: No interface was specified.")
		return False
	elif len(sys.argv) == 2:
		if sys.argv[1].isalnum():
			if os.path.isdir(STATS_DIR + "/" + sys.argv[1] + ""):
				return True
			else:
				print("ERROR: Interface does not exist.")
				return False
		print("ERROR: Interface must be alphanumeric.")
		return False
	else:
		print("ERROR: Invalid argument(s).")
		return False

def get_data():
	"""
		Returns value from a file inside of /statistics assuming 
		INTERFACE is present
	"""
	adapter = sys.argv[1]
	rx_bytes = int(open(STATS_DIR + "/" + adapter + "/statistics/rx_bytes").read().replace("\n", ""))
	tx_bytes = int(open(STATS_DIR + "/" + adapter + "/statistics/tx_bytes").read().replace("\n", ""))
	time.sleep(1)
	rx_bytes_2 = int(open(STATS_DIR + "/" + adapter + "/statistics/rx_bytes").read().replace("\n", ""))
	tx_bytes_2 = int(open(STATS_DIR + "/" + adapter + "/statistics/tx_bytes").read().replace("\n", ""))
	received_gb = round(rx_bytes_2 / 1024 ** 3, 5) 
	sent_gb = round(tx_bytes_2 / 1024 ** 3, 5)
	try:
		link_speed = round(((rx_bytes_2 + tx_bytes_2) - (rx_bytes + tx_bytes)) / 1024 ** 2, 5)
	except ZeroDivisionError:
		link_speed = 0.0
	try:
		link_speed_recv = round((rx_bytes_2 - rx_bytes) / 1024 ** 2, 5)
	except ZeroDivisionError:
		link_speed_recv = 0.0
	try:
		link_speed_sent = round((tx_bytes_2 - tx_bytes) / 1024 ** 2, 5)
	except ZeroDivisionError:
		link_speed_sent = 0.0
	
	print("--- Statistics for " + adapter + " ---")
	print("Link speed: " + str(link_speed) + " MB/s")
	print("Currently recieving: " + str(link_speed_recv) + " MB/s")
	print("Currently sending: " + str(link_speed_sent) + " MB/s")
	print("Total recieved: " + str(received_gb) + " GB")
	print("Total sent: " + str(sent_gb) + " GB")

if check_adapter():
	get_data()
else:
	print("Usage: " + sys.argv[0] + " <interface_name>")
print("")

