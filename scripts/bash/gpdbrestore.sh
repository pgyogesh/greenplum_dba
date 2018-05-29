#!\bin\bash
while getopts u:t:h option
do
 case "${option}"
 in
 u) DIRECTORY=${OPTARG};;
 t) TIMESTAMP=${OPTARG};;
 h) echo $HELP
 esac
done
