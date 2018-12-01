from text_if import text_book
import re

def same(result):
	ret = []
	for s1 in result:
		num = float(100000.0)
		_idx = 0
		s1 = s1.rstrip("\n")
		s1 = re.sub('[-=.#/?:$)}0-9|]', '', s1)
		s1 = " ".join(s1.split())
		#print("CHANGE: " + s1)
		for idx, s2 in enumerate(text_book): 
			temp = levenshteinDistance(s1, s2)
			#set1 = make_set2(s1)
			#set2 = make_set2(s2)
			#temp = len(set1 & set2) / len(set1 | set2)
			#temp = compute_jaccard_similarity_score(set1, set2)
			if(num > temp):
				num = temp
				_idx = idx
		ret.append(text_book[_idx])
	return ret


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def compute_jaccard_similarity_score(x, y):
    """
    Jaccard Similarity J (A,B) = | Intersection (A,B) | /
                                    | Union (A,B) |
    """
    intersection_cardinality = len(set(x).intersection(set(y)))
    union_cardinality = len(set(x).union(set(y)))
    return intersection_cardinality / float(union_cardinality)


def make_set2(s1):
    myset = {s1}
    test = s1.split(" ")
    for idx, item in enumerate(test):
        text = item
        for j, item2 in enumerate(test):
            if(idx == j):
                continue
            myset.add(item)
            text = item + text
    return myset
