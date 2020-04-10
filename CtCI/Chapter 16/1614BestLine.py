def build_line(p1, p2):
	if p2[0] == p1[0]:
		slope = None
		intercept = p1[0]
	elif p2[1] == p1[1]:
		slope = 0
		intercept = p1[1]
	else:
		slope = round((p2[1] - p1[1]) / (p2[0] - p1[0]), 3)
		intercept = round(p1[1] - slope * p1[0], 3)
	return intercept, slope

def best_line(graph:list): #assume graph is given as a list of paired numbers
	lines = {}
	for i, p1 in enumerate(graph):
		for p2 in graph[i+1:]:
			intercept, slope = build_line(p1, p2)
			lines.setdefault((intercept, slope), set())
			lines[(intercept, slope)].add(p1)
			lines[(intercept, slope)].add(p2)

	max_size = len(max(lines.values(), key=lambda x: len(x)))
	return max_size, [points for points in lines.values() if len(points) == max_size]

if __name__ == "__main__":
	import sys
	from random import randint
	point_count = int(sys.argv[1])
	
	graph = [(randint(-10, 10), randint(-10, 10)) for _ in range(point_count)]	
	print(graph)
	print(best_line(graph))
	