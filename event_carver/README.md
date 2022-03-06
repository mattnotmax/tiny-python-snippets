# event_carver

Used to search binary data for x\2Ax\2Ax\00x\00 and then carve out the EVTX information. For more details see https://bitofhex.com/2018/05/10/memory-forensics-tor-part-two/

Requires: Python 3

Usage: event_carver.py \<filename\>

It will create an `./output` directory with a summary CSV and carved event data.

Ths program is provided as-is and with no warranty under MIT license. At this stage it has not undergone significant testing against wider datasets. 

**Please use at your own risk.**
