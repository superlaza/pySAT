from collections import deque

var_dict = {}
var_list = []
clauses = []
with open('input.txt') as f:
	for clause in f.readlines():
		_clause = []
		for literal in clause.split():
			neg = 1 if literal.startswith('-') else 0
			var = literal[neg] # if it's negative, the actual variable is @ pos 1

			if var not in var_dict:
				var_dict[var] = len(var_list) # index is current length of var list
				var_list.append(var)
			# assign index to variables literal by bitwise shift right (x2) <<, then negate if necessary
			encoded = var_dict[var] << 1 | neg

			_clause.append(encoded)
		clauses.append(_clause)
print var_list
print var_dict
print clauses

print set([item for sublist in clauses for item in sublist])


# initialize watchlist using fast double-ended queues
watchlist = [deque() for __ in range(2 * len(var_list))]
print watchlist
for clause in clauses:
	# clause watches its first literal
	watchlist[clause[0]].append(clause)

print watchlist

# all literals being watched are either not assigned yet or have a true assignment
def update_watchlist(watchlist, false_literal, assignment):
	runcount = 0
	while watchlist[false_literal]:
		print 'watchlist', watchlist
		# print runcount
		runcount += 1
		clause = watchlist[false_literal][0]
		print 'false_literal', false_literal, '--', 'clause watching', clause
		found_alternative = False
		for alternative in clause:
			v = alternative >> 1 # get var from literal
			a = alternative & 1 # a bitwise AND checks to see literal var is negated (basically odd or even check)
			print 'alternative', alternative, 'var', v, '- is neg?: ', a
			print assignment
			if assignment[v] is None or assignment[v] == a ^ 1: # XOR, basically opposite of a
				found_alternative = True
				del watchlist[false_literal][0]
				watchlist[alternative].append(clause)
				break
		# if we run through all alternatives in the given clause without finding alt
		if not found_alternative:
			return False
	return True

runcount = 0
def solve(watchlist, assignment, d):
	if d == len(var_list):
		yield assignment
		return

	for a in [0, 1]:
		assignment[d] = a
		if update_watchlist(watchlist, (d << 1) | a, assignment):
			for a in solve(watchlist, assignment, d + 1):
				yield a

	assignment[d] = None

n = len(var_list)
assignment = [None for _ in range(n)]
# print update_watchlist(watchlist, n, assignment)
res = solve(watchlist, assignment, 0)
# print 'res', res
for r in res:
	print 'solved', r

# for assignment in res:
# 	print assignment