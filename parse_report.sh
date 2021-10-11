#!/data/data/com.termux/files/usr/bin/bash

out_dir=/data/data/com.termux/files/home/storage/pictures
now=`date +%Y%m%d-%H%M%S`
python parse_report.py

ls out*
mv out* ${out_dir}/



