def expection():
	sum = 0
	for i in range(4):
		for j in range(4):
			sum += (i+1)*(j+1)
	return sum/16.0
print expection()