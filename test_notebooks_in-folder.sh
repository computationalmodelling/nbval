for FILE in $(find $1 -not -path '*/\.*' -path '*.ipynb')
do
	echo "\n"
	echo "=========== TESTING $(echo $FILE | grep "\w*\.ipynb") ==============\n"
        echo "===================================================================\n"	
	./parsenb.py $FILE
done
