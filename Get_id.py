from rotten_tomatoes_client import RottenTomatoesClient

def get_id(Term):

	result = RottenTomatoesClient.search(term=Term, limit=5)
	movie = result['movies'][0]
	id = movie['url'].split('/')[-1]
	print (id)
	#print (len(result['movies']))
	return id