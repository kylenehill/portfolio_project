import requests

# Make a GET request to the /api/tasks endpoint
response = requests.get('http://127.0.0.1:5000/api/tasks')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract tasks data from the JSON response
    tasks_data = response.json()['tasks']
    # Process the tasks data as needed
    for task in tasks_data:
        print(task)
else:
    print('Failed to retrieve tasks:', response.status_code)