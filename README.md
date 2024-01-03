
# Port scanner

This project made in python3.10 and is made to exercice my programming skill while learning how cybersecurity tool work.
## Usage/Examples


```shell
$ python3 -h

Usage: python3 port_scanner.py <mode> <subnet/netmask> 
Modes:
--ping_sweep or -ps to perform a ping check on addresses in the subnet
--port_scan or -s (under construction)
-v for verbose mode (display error when an ip doesn't respond)
Example: python3 port_scanner.py --ping_sweep 192.168.1.0/24
```

```shell
$ python3 port_scanner --ping_sweep 192.168.1.0/24

Address to scan : 192.168.1.0
Netmask :  255.255.255.0
there are 256 addresses to scan
Found :  192.168.1.1
Found :  192.168.1.23
Found :  192.168.1.11
Found :  192.168.1.13
Found :  192.168.1.45
Found :  192.168.1.55
Found :  192.168.1.64
```


## Roadmap

1. add an option ip ranges/list more than subnets
2. add an option to set the number of threads
3. add an option of file output
4. add an option of input file
5. add an option to set the ports to scan (precise not range)
6. add an option to set the timeout
7. add an option to set the number of retries
8. add an option to enable or disable the banner grabbing 
9. check if ip is reachable before scanning
10. improve banner grabbing to vary the message send based on the port scanned

## Authors

- [@victor-minne](https://www.github.com/victor-minne)

