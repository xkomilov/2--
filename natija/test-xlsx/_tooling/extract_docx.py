#!/usr/bin/env python3
"""Extract plain text from a .docx file by reading word/document.xml."""
import sys, zipfile, re
from xml.etree import ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def extract(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    lines = []
    body = root.find('w:body', NS)
    for p in body.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = []
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            texts.append(t.text or '')
        line = ''.join(texts).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)

if __name__ == '__main__':
    print(extract(sys.argv[1]))
