#!/usr/bin/env python

__version__ = "0.1"
__description__ = "Calculate MD5 & SHA1 hash from file using a 64KB buffer"

import sys
import os
import hashlib
import argparse

def process_arguments():
    # Establish commond line arguments
    parser = argparse.ArgumentParser(description='{}, version: {}'
    .format(__description__, __version__))
    parser.add_argument('filename', help='A target filename')
    parser.add_argument('-s', '--sha256', action='store_true',
                        default=False, help='Calculate SHA256 value in addition to MD5 & SHA1')
    args = parser.parse_args()
    filename = args.filename
    sha256_setting = args.sha256
    return(filename, sha256_setting)

def hash_file(filename, sha256_setting):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    buffer = 65536
    file_size = os.path.getsize(filename)
    chunks = file_size / buffer
    progress = 0.0

    with open(filename, 'rb') as f:
        while True:
            data = f.read(buffer)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            if sha256_setting == True:
                sha256.update(data)
            # loop to calculate per cent completed unless only one chunk
            if chunks <= 1:
                continue
            else:
                percent_progress = (progress / chunks) * 100
                print('Hashing: {:.2f}%'.format(percent_progress), end='\r')
                sys.stdout.flush()
                progress += 1

    #Output hashes to stdout
    if sha256_setting == False:
        print('\nFilename:\t{}\nMD5:\t\t{}\nSHA1:\t\t{}'.format(filename,
        md5.hexdigest(),sha1.hexdigest()))
    else:
        print('\nFilename:\t{}\nMD5:\t\t{}\nSHA1:\t\t{}\nSHA256\t\t{}'
        .format(filename, md5.hexdigest(),sha1.hexdigest(), sha256.hexdigest()))

def main():
    filename, sha256_setting = process_arguments()
    hash_file(filename, sha256_setting)


if __name__== "__main__":
    main()
