import unittest


def build_reverse_mapping(docs):
	rev_map = {}
	for did, words in docs.items():
		for w in words:
			rev_map.setdefault(w, [])
			rev_map[w].append(did)
	return rev_map

def similar_docs(revmap):
	gen = (didlist for didlist in revmap.values() if len(didlist) > 1)
	for didlist in gen:
		for i in range(len(didlist) - 1):
			for j in range(i+1, len(didlist)):
				doc1, doc2 = didlist[i], didlist[j]				
				yield min(doc1, doc2), max(doc1, doc2)
		
def sparse_similarity(documents:dict):
	similarities = {}
	revmap = build_reverse_mapping(documents)
	for (d1, d2) in similar_docs(revmap):
		if (d1, d2) not in similarities:
			insecsize = len(set(documents[d1]).intersection(set(documents[d2])))
			unionsize = len(set(documents[d1]).union(set(documents[d2])))
			similarities[(d1, d2)] = insecsize / unionsize
	return similarities


class Test(unittest.TestCase):
	documents = {13:[14, 15, 100, 9, 3], 16:[32, 1, 9, 3, 5], 19:[15, 29, 2, 6, 8, 7], 24:[7, 10]}
	result = {(13, 19): 0.1, (13, 16):0.25, (19, 24): 0.14285714285714285}

	def test_sparse_similarity(self):
		output = sparse_similarity(self.documents)
		self.assertEqual(output, self.result)


if __name__ == '__main__':
	unittest.main()
	