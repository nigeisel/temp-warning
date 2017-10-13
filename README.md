# temp-warning
Command line tool that checks CPU temperature and warns if it's too high

# Usage

usage: temp-warning [-h] [-t temperature] [-i interval] [-b] [-l]

optional arguments:

  -h, --help      show this help message and exit
  
  -t temperature  temperature that is considered critical in °C
  
  -i interval     interval to check temp in s
  
  -b              activate beep on crit temp (default: no beep)
  
  -l              deprecated
