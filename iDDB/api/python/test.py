import csv
i = 0
with open('innovators.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "NAME", "STUDENT"])
    for i in range(0, 30):
	if i % 2 == 0:
		writer.writerow([i, "Andrei", "false"])
	else:
		writer.writerow([i, "Furdui", "true"])
