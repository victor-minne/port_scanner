
# Port scanner

This project made in python3.10 and is made to exercice my programming skill while learning how cybersecurity tool work.
## Usage/Examples


```shell
$ python3 main.py -h

usage: main.py [-h] [--ping_sweep] [--port_scan] [--verbose] [--banner_grabbing] [-ip IP] [--port_range PORT_RANGE] [--net_mask NET_MASK]

Port scanner

options:
  -h, --help            show this help message and exit
  --ping_sweep, -ps     Perform a ping sweep
  --port_scan, -s       Scan a single target
  --verbose, -v         Verbose mode
  --banner_grabbing, -b
                        Banner grabbing
  -ip IP                IP or hostname to scan
  --port_range PORT_RANGE, -p PORT_RANGE
                        Max port to scan
  --net_mask NET_MASK, -m NET_MASK
                        Subnet to scan
```

```shell
python3 main.py -s -b -ip 192.168.1.171 -p 1000
__________________________________________________
Address to scan: 192.168.1.100
There are 1000 ports to scan
Using 254 thread to do so 
__________________________________________________ 

Port 80		[open]
Service: 
Banner: HTTP/1.1 200 OK
Date: Sat, 10 Feb 2024 19:53:52 GMT
Connection: close
Content-type: text/html
Accept-Ranges: bytes
Last-Modified: Sat, 13 Nov 2021 04:18:52 GMT
ETag: "618f3cac-1b7"
Content-Length: 439

<pre>
Hello World


                                       ##         .
                                 ## ## ##        ==
                              ## ## ## ## ##    ===
                           /""""""""""""""""\___/ ===
                      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
                           \______ o          _,/
                            \      \       _,'
                             `'--.._\..--''
</pre>

Port 111		[open]
Service: 
Banner: 
Port 902		[open]
Service: 
Banner: 
Scan complete, 1000 ports scanned

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
9. Done  check if ip is reachable before scanning
10. improve banner grabbing to vary the message send based on the port scanned

## Authors

- [@victor-minne](https://www.github.com/victor-minne)

