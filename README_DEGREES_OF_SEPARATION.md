# Degrees of separation

A document that discusses the degrees of separation functionality


### Requirements

1. Given a valid person id and an integer x representing "degrees of separation" it should return a list of people connected within x degrees of separation to that person.

2. Should be based on the “six degrees of separation” concept ([link text itself]: https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon).


### Input Fields

1. person_id : Integer : Mandatory
2. degree : Integer : Mandatory


### Endpoint

	[link text itself]: /people/<people_id>/degree/<degree>


### Response

	Returns the list of person objects

```json
	[
	  {
	    "created_at": "2021-04-14T04:11:51+00:00", 
	    "date_of_birth": "2010-02-02", 
	    "email": "test1@test.com", 
	    "first_name": "TestF1", 
	    "id": 1, 
	    "last_name": "TestF1", 
	    "updated_at": "2021-04-14T04:11:51+00:00"
	  },
	  
	  ....

	  {
	    "created_at": "2021-04-14T04:12:41+00:00", 
	    "date_of_birth": "2000-01-01", 
	    "email": "test2@test.com", 
	    "first_name": "TestF2", 
	    "id": 2, 
	    "last_name": "TestF2", 
	    "updated_at": "2021-04-14T04:12:41+00:00"
	  }
	]
```

### Design Concept

1. Endpoint should expect to receive two integer fields: person_id and degree
2. Check whether the person exists in the database. Raise validation error if the person does not exist.
3. If the person exist already, then find the connections of the person
4. Create a recursive method to get connections of person which takes a reference of an empty list (Say connected_people) and the degree as input 
5. During each recursive iteration check whether the connection type is of interest if required and reduces the degree input by 1
6. Each time the recursive function is called, it adds the connected person in the connected_people list
7. The method stops when the degree value is -1. Thus making sure that method is called the given degree of seperation from each degree of seperation
8. The recursive method returns filled connected_people list


### Potential technical challenges

1. Whenever a new connection type is added the connection types of interest changes
2. It can lead to memory leaks if degree is high.


### Recommendation

1. Should be easier if a recursive method is developed
2. Consider adding garbage collector if degree is high


### Questions

1. What will be definition for interested connection type for each connection type?
2. What will be highest degree which will be given?