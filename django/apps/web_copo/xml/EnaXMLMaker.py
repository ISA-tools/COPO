__author__ = 'fshaw'
import xml.etree.ElementTree as ET

def make_submissions(c):
    root = ET.Element("html")


    tree = ET.ElementTree(root)
    tree.write('/Users/fshaw/Desktop/root.xml')