def shuffle(deck, rand_function):	

	for i in range(len(deck)):
		randindex = rand_function(i, len(deck)-1) #inclusive
		temp = deck[i]
		deck[i] = deck[randindex]
		deck[randindex] = temp


if __name__ == "__main__":
	from random import randint
	cards = list(range(1, 53))
	shuffle(cards, randint)
	print(cards)