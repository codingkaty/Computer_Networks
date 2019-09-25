#!/bin/biash        
lineNum=1

for file in *;
do
	if [ "$file" = test.sh ];then
		continue
	fi
		while read line
		do
			counter=$((lineNum%2))
				if [ $counter -eq 0 ];then
				
					echo "$file: $line"
				fi
				((lineNum++))
		
		done < $file
		lineNum=1
	
done


