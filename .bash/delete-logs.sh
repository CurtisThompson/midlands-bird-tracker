# Get current date as string in format of log files
currentdate=$(date -d "$date -30 days" +"%Y%m%d")

# Remove logs older than a month
for file in ./.log/*.txt; do
    if [ ${file:7:8} -le $currentdate ]
    then
        rm $file;
    fi
done