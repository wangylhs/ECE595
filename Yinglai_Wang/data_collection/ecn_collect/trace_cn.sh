#!/bin/bash
count=0

while read line; do
	array[$count]=$line;
	let count=count+1;
done < ~/ECE595/main_project/web/cnweb.txt

for element in ${array[@]}
do
	#echo $element
	date >> ~/ECE595/main_project/data/data_cn
	traceroute 2>&1 -m 20 $element | awk -v OFS='\n' '{if(NR!=1){print $1 " " $3 " " $4}else{print $3 " " $4}}' >> ~/ECE595/main_project/data/data_cn

done
