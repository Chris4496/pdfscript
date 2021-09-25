from distutils.core import setup
import py2exe
from PyPDF2 import PdfFileReader, PdfFileWriter
import csv
import os
import main

setup(console=['gui.py'])
