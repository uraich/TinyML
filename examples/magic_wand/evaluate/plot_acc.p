set title 'acceleration data'
plot for [col=1:3] 'no_acceleration.txt' using 0:col with lines title columnheader
