from distutils.core import setup
import py2exe
from PyPDF2 import PdfFileReader, PdfFileWriter
import csv
import os


setup(console=['main.py'])
