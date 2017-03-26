# Cab Sharing

This is source for api of cab-sharing feature for the KGP dashboard

## Getting Started

- Install all the dependancies 
```
pip install -r requirements.txt
```
### How to run 

```
python app.py
```

## Basic API endpoints

 > /get-all-cabs  
 	This endpoint returns all the cabs 
 	Parameters Required : 
 		None 
	Parameters Returned : 
		success : Boolean (Whether the request was a success or not)
		data    : JSON i.e. a list of Dictionaries, (if success == True)
				  Parameter of dictionary : name = Name of person who posted the cab 
											email = Email of person who posted the cab
											number = Contact Number of person who posted the cab
											availSeats=Available seats in the cab 
											dest=Destination	
											date=Date of Journey
											time=Time of Journey
											threshold = Threshold of time

> /search-cab , method : POST
	This end point returns all the cabs that have the same destination and times lies between posted time +/- threshold
	Parameters Required :
		dest : String - The destination of the user
		date : Proper date in the format "YYYY-MM-DD"
		time : Proper time in the 24 Hour format "HH:MM" 
	Parameters Returned : 
		success : Boolean (Whether the request was a success or not)
		data 	: JSON i.e. a list of Dictionaries,  (if success == True)
				  Parameter of dictionary : name = Name of person who posted the cab 
											email = Email of person who posted the cab
											number = Contact Number of person who posted the cab
											availSeats=Available seats in the cab 
											dest=Destination
											threshold = Threshold of time

> /post-cab , method : POST
	This endpoint is used to add a cab to the database
	Paramenters Required : 
		name = Name of person who posted the cab 
		email = Email of person who posted the cab
		number = Contact Number of person who posted the cab
		availSeats=Available seats in the cab 
		dest=Destination	
		date=Date of Journey
		time=Time of Journey
		threshold = Threshold of time
	Parameters Returned : 
		success : Boolean (Whether the request was a success or not)

