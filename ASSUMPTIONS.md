### Assumptions

1. There can be multiple connections between the same from_person and to_person combination.
	eg: person A can be dad of person B; person A and person B can be coworkers
2. There won't be multiple connections with the same from_person, to_person and connection_type
3. The connection_type is in the perspective of from_person
	eg: {from_person: 'A', to_person: 'B', connection_type: 'son'} implies that the person A is the son of person B