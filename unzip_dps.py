# unzip ru and sbs-pd from local folder /share/ in the GoldenDict folder

import os
import glob

from datetime import date
from zipfile import ZipFile

today = date.today()

# Print starting message
print("\033[33m from dps/exporter/share/ \033[0m")

sbs_pd_path = 'share/sbs-pd.zip'
if os.path.exists(sbs_pd_path):
   with ZipFile(sbs_pd_path, 'r') as zipObj:
      # Extract all the contents of zip file in current directory
      zipObj.extractall('../../GoldenDict')

   # Print completion message in green color
   print("\033[32m sbs-pd.zip has been unpacked to the GoldenDict folder \033[0m")

else:
   print(f"\033[31mWarning: {sbs_pd_path} not found. Skipping extraction.\033[0m")

# Removing all files starting with sbs-pd.zip. from the same directory
for f in glob.glob("share/sbs-pd.zip.*"):
   os.remove(f)

ru_pali_dictionary_path = 'share/ru-pali-dictionary.zip'
if os.path.exists(ru_pali_dictionary_path):
   with ZipFile(ru_pali_dictionary_path, 'r') as zipObj:
      # Extract all the contents of zip file in current directory
      zipObj.extractall('../../GoldenDict')

   # Print completion message in green color
   print("\033[32m ru-pali-dict.zip has been unpacked to the GoldenDict folder \033[0m")

else:
   print(f"\033[31mWarning: {ru_pali_dictionary_path} not found. Skipping extraction.\033[0m")

# Removing all files starting with ru-pali-dictionary.zip. from the same directory
for f in glob.glob("share/ru-pali-dictionary.zip.*"):
   os.remove(f)

dps_path = 'share/dps.zip'
if os.path.exists(dps_path):
   with ZipFile(dps_path, 'r') as zipObj:
      # Extract all the contents of zip file in current directory
      zipObj.extractall('../../GoldenDict')

   # Print completion message in green color
   print("\033[32m dps.zip has been unpacked to the GoldenDict folder \033[0m")

else:
   print(f"\033[31mWarning: {dps_path} not found. Skipping extraction.\033[0m")

# Removing all files starting with dps.zip. from the same directory
for f in glob.glob("share/dps.zip.*"):
   os.remove(f)
