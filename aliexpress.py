#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import requests, os
from urllib3 import encode_multipart_formdata
from concurrent.futures import ThreadPoolExecutor, as_completed
 
def m_upload(filename):
    fakename = os.path.splitext(filename)[0] + '.jpg'
    payload = {'scene':'aeMessageCenterV2ImageRule', 'name':fakename, 'file': (fakename,open(filename,'rb').read())}
    encode_data = encode_multipart_formdata(payload)
    data = encode_data[0]
    headers['Content-Type'] = encode_data[1]
    for _ in range(3):
        try:
            r = requests.post(url, headers=headers, data=data, timeout = 20)
        except:
            print('Failed to upload ' + filename)
            continue
        if r and 'url' in r.text:
            print(filename + " upload")
            return r.json()['url']
        else:
            print('Failed to upload ' + filename)
    return filename + ' ERROR'
 
if __name__ == '__main__':
    for file in os.listdir():
        if '.m3u8' in file:
            m3u8 = open(file)
            break
    new_m3u8 = open('output.m3u8', 'w')
    headers = {'user-agent':'iAliexpress/6.22.1 (iPhone; iOS 12.1.2; Scale/2.00)', 'Accept':'application/json', 'Accept-Encoding':'gzip,deflate,sdch', 'Connection':'close'}
    url = 'https://kfupload.alibaba.com/mupload'
    file_upload = {t.strip():'' for t in m3u8.readlines() if t[0]!='#'}
    m3u8.seek(0)
    executor = ThreadPoolExecutor(max_workers=8)
    futures = {executor.submit(m_upload, filename):filename for filename in file_upload.keys()}
    for future in as_completed(futures):
        file_upload[futures[future]] = future.result()
    for line in m3u8:
        if line[0] != '#':
            new_m3u8.write(file_upload[line.strip()] + 'n')
        else:
            new_m3u8.write(line)
    