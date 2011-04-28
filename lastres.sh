# Finds the last result in the `results/` directory, pipes to less

LASTFILE=$(ls results/ | sort -r | head -n 1)
less results/$LASTFILE
