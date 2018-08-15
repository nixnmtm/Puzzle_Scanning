#!/bin/bash

# Run this script to setup puzzle scanning in device and server
# eg: pzl_ScanSetup.sh d --------> Device Side
#     pzl_ScanSetup.sh s --------> Server Side

date
echo 8888 | sudo -S su
cd ~
rm -rf Puzzle_Scanning
git clone -b PuzzleScanDev --single-branch http://40.74.91.221/puzzle/device-intel-factory.git Puzzle_Scanning
cd Puzzle_Scanning

# Device side setup
if [$1 == "d"]
then ./setup_dScanning.sh
fi

# Server side setup
if [$1 == "s"]
then ./setup_sScanning.sh
fi

exit

