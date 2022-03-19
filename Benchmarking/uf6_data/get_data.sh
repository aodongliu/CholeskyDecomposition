# This script can process the ERI data and spit out numbers we want to analyze

# User need to provide the file name as the argument. Filename will be read in as $1

echo Step 1 Data:
grep 'Cholesky-RI-Pivots-ERI count' -A 11 $1 | awk '{print $4}'

echo ----------------------------------------------------------

echo Step 2 Data:
grep "Build 3-index RIERI tensor:" -A 11 $1 | grep -v "Build 3-index RIERI tensor:" | grep -v "\-\-" | awk '{print $4}'


echo ----------------------------------------------------------

echo Total Time:
grep 'Cholesky-RI duration =' $1| awk '{print $4}'

echo ----------------------------------------------------------

echo Other Information:
grep 'NBasis' $1 | awk '{print $2}'
grep 'NPrimitive' $1 | awk '{print $2}'
grep 'NShell' $1 | awk '{print $2}'
grep 'Max Primitive' $1 | awk '{print $3}'
grep 'Max L' $1 | awk '{print $3}'
grep 'nsmp =' $1 | awk '{print $3}'
grep 'mem =' $1 | awk '{print $3}'
grep '\- Memory allocation' $1 | awk '{print $5}'
