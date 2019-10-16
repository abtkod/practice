def tower_of_hanoi(disk_count, tow1, tow3, tow2):
	if disk_count == 1:
		disk = tow1.pop()
		tow3.append(disk)
		return

	if disk_count == 2:
		disk = tow1.pop()
		tow2.append(disk)
		disk = tow1.pop()
		tow3.append(disk)
		disk = tow2.pop()
		tow3.append(disk)
		return

	tower_of_hanoi(disk_count-1, tow1, tow2, tow3)	
	disk = tow1.pop()
	tow3.append(disk)
	tower_of_hanoi(disk_count-1, tow2, tow3, tow1)
	return


tower1, tower2, tower3 = list(reversed(range(1, 16))), [], []
print(tower1, tower2, tower3)
tower_of_hanoi(len(tower1), tower1, tower3, tower2)
print(tower1, tower2, tower3)