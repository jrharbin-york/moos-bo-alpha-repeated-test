for i in {1..300}
do
	./launch.sh
	sleep 70
# This is the wait with a run time of 1200, warp 20, plus wait factor
	./terminate.sh
done
