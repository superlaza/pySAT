from collections import deque

var_dict = {}
var_list = []
clauses = []
with open('input.txt') as f:
	for clause in f.readlines():
		_clause = []
		for literal in clause.split():
			neg = 1 if literal.startswith('-') else 0
			var = literal[neg]

			if var not in var_dict:
				var_dict[var] = len(var_list) # index is current length of var list
				var_list.append(var)
			# assign index to variables literal by bitwise shift right (x2) <<, then negate if necessary
			encoded = var_dict[var] << 1 | neg

			_clause.append(encoded)
		clauses.append(_clause)

print clauses

# initialize watchlist using fast double-ended queues
watchlist = [deque() for __ in range(2 * len(var_list))]
print watchlist
for clause in clauses:
	# unpack clause and add it to watchlist
	watchlist[clause[0]].append(clause)

# all literals being watched are either not assigned yet or have a true assignment
def update_watchlist(watchlist, false_literal, assignment):
	runcount = 0
	while watchlist[false_literal]:
		print runcount
		runcount += 1
		clause = watchlist[false_literal][0]
		found_alternative = False
		for alternative in clause:
			v = alternative >> 1 # get var from literal
			a = alternative & 1 # an AND checks to see literal var is negated
			if assignment[v] is None or assignment[v] == a ^ 1:
				found_alternative = True
				del watchlist[false_literal][0]
				watchlist[alternative].append(clause)
				break
		if not found_alternative:
			return False
	return True

runcount = 0
def solve(watchlist, assignment, d):
	if d == len(var_list):
		print assignment
		yield assignment
		return

	print runcout
	runcout += 1
	for a in [0, 1]:
		assignment[d] = a
		if update_watchlist(watchlist, (d << 1) | a, assignment):
			for a in solve(watchlist, assignment, d + 1):
				print a
				yield a

	assignment[d] = None
n = len(var_list)
assignment = [None]*n
print update_watchlist(watchlist, n, assignment)
res = solve(watchlist, assignment, 0)
print 'res',res
for assignment in res:
	print assignment