# unzip ru and sbs-pd from local folder /share/ in the GoldenDict folder

import os
import glob

from datetime import date
from zipfile import ZipFile

today = date.today()

# Print starting message
print("\033[33m from dps/exporter/share/ \033[0m")

with ZipFile('share/sbs-pd.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall('../../GoldenDict')

# Print completion message in green color
print("\033[32m sbs-pd.zip has been unpacked to the GoldenDict folder \033[0m")

# Removing all files starting with sbs-pd.zip. from the same directory
for f in glob.glob("share/sbs-pd.zip.*"):
   os.remove(f)

with ZipFile('share/ru-pali-dictionary.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall('../../GoldenDict')

# Print completion message in green color
print("\033[32m ru-pali-dict.zip has been unpacked to the GoldenDict folder \033[0m")

# Removing all files starting with ru-pali-dictionary.zip. from the same directory
for f in glob.glob("share/ru-pali-dictionary.zip.*"):
   os.remove(f)

# Removing all files starting with ru-pali-dictionary-full.zip. from the same directory
for f in glob.glob("share/ru-pali-dictionary-full.zip.*"):
   os.remove(f)
