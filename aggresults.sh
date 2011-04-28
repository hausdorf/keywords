# Gets results for most recent run of algorithm, records results, places
# results in the `results/` directory.

cd trial

TIMESTAMP=$(perl -e "print time")
FILENAME=out${TIMESTAMP}
perl performance.pl ../results.stm > $FILENAME
mv $FILENAME ../results/$FILENAME

cd ..
