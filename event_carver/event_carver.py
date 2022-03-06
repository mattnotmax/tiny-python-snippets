import struct
import sys
import csv
from datetime import datetime, timedelta
import os

with open(sys.argv[1], 'rb') as file_open:
    filecontent = file_open.read()

# Create output directory
directory = './output'
if not os.path.exists(directory):
    os.makedirs(directory)

# Establish search string for event record fragment
searchstring = "\x2A\x2A\x00\x00"
nexthit = filecontent.find(searchstring.encode('utf-8'), 0)
hitlist = []

# Locate event record fragments in file
while nexthit >=0:
    hitlist.append(nexthit)
    nexthit = filecontent.find(searchstring.encode('utf-8'), nexthit + 1)

# Set up CSV summary file
summary_file_headers = ['offset decimal', "offset hex", "event fragment size (bytes)", "event record identifer", "event record filetime (UTC +0)", "event ID"]
with open ('./output/events_summary.csv', 'w', newline='') as summary_file:
    writer = csv.writer(summary_file)
    writer.writerow([item for item in summary_file_headers])

# Loop through fragments to obtain data
for hit in hitlist:
    print("Located header at offset: " + hex(hit))
    
    # Event Log Size
    event_size_offset = hit + 4
    event_size = struct.unpack("<I",filecontent[event_size_offset:(event_size_offset+4)])[0]
    
    # Event Record Identifer
    event_record_offset = event_size_offset + 4
    event_record = struct.unpack("<I",filecontent[event_record_offset:(event_record_offset+4)])[0]
    
    # Event Record FILETIME written
    event_filetime_offset = event_record_offset + 8
    event_filetime = struct.unpack("<Q",filecontent[event_filetime_offset:(event_filetime_offset+8)])[0]
    iso_datetime = datetime(1601,1,1) + timedelta(microseconds=(event_filetime/10))
    iso_date = (str(iso_datetime))[0:10]
        
    # Event ID
    event_id_offset = hit + 118
    event_log = struct.unpack("<H",filecontent[event_id_offset:(event_id_offset+2)])[0]
    
    # Footer Event Record Size (currently not used)
    footer_event_record_offset = event_size - 4
    footer_event_record = struct.unpack("<I", filecontent[footer_event_record_offset:(footer_event_record_offset+4)])[0]
        
    # Write files to CSV summary file
    csv_data = ([str(hit), hex(hit), str(event_size), str(event_record), str(iso_datetime), str(event_log)])
    with open ('./output/events_summary.csv', 'a', newline='') as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow([data for data in csv_data])
    
    # Export event record
    file_export = filecontent[hit:(hit+event_size)]
    with open("./output/offset_" + str(hex(hit)) + "_" + iso_date + ".bin", "wb") as outfile:
        outfile.write(file_export)

# Exit with summary
date = datetime.now()
print("\nLocated " + str(len(hitlist)) + " Windows Event Record fragments")
print("Event carver completed at " + date.strftime("%H:%M:%S, %d-%b-%Y"))