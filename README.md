# ECE1779_Project1
Assignment Group 2

## Group Members and Contributions:
- [mrchenliang](https://github.com/mrchenliang)
- [BrianQJN](https://github.com/BrianQJN)
- [Heliali](https://github.com/Heliali)
### Contributions Graph
<!-- Insert Graph Here -->

## Dependencies
The assignment project requires the following libraries `Flask, gunicorn, mysql.connector, matplotlib.figure, flask_apscheduler`
### To Install
`pip3 install -r requirements.txt`
## Setup and Run
### To Start
`sh start.sh`
### To Stop
`sh shutdown.sh`

## Project Architecture
This assignment project has 2 independent flask instances
- 1 instance is for the backend service running on port 5000
- 1 instance is for the memcache service running on port 5001

The backend service returns web pages and responds to api requests. The memcache service is exposed to the public but is used as an internal service that the backend service calls to configure, add, update and reset the memcache. The memcache also updates the database periodically with the memcache data.

## Database
This assignment project uses a local mysql database to store the following database. There are 3 different tables: 1 for the images, 1 for the cache properties, and 1 for cache stats.

### Database Schema
![Database Schema](../ECE1779_Project1/static/database_schema.jpeg)

## Design Decisions

### Independent Flask Instance for Memcache and Backend
- Decision: The decision was to create 2 independent flask instances, one for the memcache, and one for the backend running on port 5001 and 5000 respectively. 
- Alternative: The alternative is to have 1 flask instance and have the memcache to run within the backend service, the downside of this is that it is a monolith architecture which is difficult with scaling as there are more opportunities to conflict and overwrite the services.
- Reason: The reason why there are 2 independent flask instances is because they can be seen as individual services that a backend could potentially refactor out to be a microservice environment. In the future development, the 2 flask instances can be developed independently without interferring with each other and the 2 flask instances will communicate using HTTP requests.

### Memcache Stats Graph Plotting
- Decision: 
- Alternative: 
- Reason:
## Graphs

### Graph 1 20:80 Read/Write Ratio Latency Graph
### Graph 2 20:80 Read/Write Ratio Throughput Graph
### Graph 3 50:50 Read/Write Ratio Latency Graph
### Graph 4 50:50 Read/Write Ratio Throughput Graph
### Graph 5 80:20 Read/Write Ratio Latency Graph
### Graph 6 80:20 Read/Write Ratio Throughput Graph
### Discussions



