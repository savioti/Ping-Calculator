import socket
import time
import sys

host = "18.224.220.128"
port = 6000

packages_lost = 0
ping_iterations = 10
timeout = 0.25
interval = 1
ping_count = 0
ping_time_sum = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)

message = "Executing operation..."
message = message.encode()

def calculate_average_rtt():
    average_rtt = 0

    if ping_count > 0:
        average_rtt = ping_time_sum / ping_count

    print('Average RTT ' + str(round(average_rtt, 2)) + 'ms')

def calculate_package_loss():
    package_loss_rate = 0;

    if ping_iterations > 0:
        package_loss_rate = packages_lost / ping_iterations

    print('Package loss rate: ' + str(round(package_loss_rate, 2)))

time_start = time.time()

for i in range(ping_iterations):
    try:
        client_socket.sendto(message, (host, port))
        start = time.time()
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        elapsed = (end - start) * 1000
        ping_count += 1
        ping_time_sum += elapsed
        time.sleep(interval)
        print('Iteration ' + str(i))
    except socket.timeout as e:
        packages_lost += 1
        print('Iteration ' + str(i) + ' failed')
    except KeyboardInterrupt:
        calculate_average_rtt()
        calculate_package_loss()

calculate_average_rtt()
calculate_package_loss()