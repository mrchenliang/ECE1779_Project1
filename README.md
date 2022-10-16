<div id="top"></div>
<h3 align="center">ECE1779 Project 1</h3>
  <p align="center">
    Introduction to Cloud Computing
    <br />
  </p>
</div>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Getting-Started">Getting Started</a>
      <ul>
        <li><a href="#Dependencies">Dependencies</a></li>
        <li><a href="#Installation">Installation</a></li>
        <li><a href="#Source-Database">Source Database</a></li>
        <li><a href="#Setup-and-Run">Setup and Run</a></li>
      </ul>
    </li>
    <li><a href="#Project-Architecture">Project Architecture</a></li>
      <ul>
        <li><a href="#Web-Pages-Port-5000">Web Pages</a></li>
        <li><a href="#Backend-API-Endpoints-Port-5000">Backend API Endpoints</a></li>
        <li><a href="#Memcache-API-Endpoints-Port-5001">Memcache API Endpoints</a></li>
      </ul>
    <li><a href="#Database">Database </a></li>
    <li><a href="#Design-Decisions">Design Decisions </a></li>
    <li><a href="#Graphs">Graphs </a></li>
    <li><a href="#Discussions">Discussions </a></li>
    <li><a href="#Group-Members-and-Contributions">Group Member and Contributions</a></li>
  </ol>
</details>

## Getting Started
### Dependencies
The assignment project requires the following libraries `Flask, gunicorn, requests, mysql.connector, matplotlib.figure`
### Installation
`git clone https://github.com/mrchenliang/ECE1779_Project1.git`
`pip3 install -r requirements.txt`
### Source Database
`mysql -u admin -p ece1779`
`mysql> source database/memcache.sql`
### Setup and Run
### To Start
`sh start.sh`
### To Stop
`sh shutdown.sh`

## Project Architecture
This assignment project has 2 independent flask instances
- 1 instance is for the backend service running on port 5000
- 1 instance is for the memcache service running on port 5001

The backend service returns web pages and responds to api requests. The memcache service is exposed to the public but is used as an internal service that the backend service calls to configure, add, update and reset the memcache. The memcache also updates the database periodically with the memcache data. The memcache stores the key and the image in base64 and can supports both Least Recently Used and Random Replacement methods.

### Web Pages (Port 5000)
- `/` directs to home page
- `/image` directs to get image page
![Get Image Hit](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/get%20image%20hit%20%26%20post%20clear_cache.jpeg)
![Get Image Miss](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/get%20image%20miss.jpeg)

- `/upload_image` directs to put image page
![Post Upload Image](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/post%20upload_image.jpeg)

- `/keys_list` directs to get keys list page
![Get Keys List](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/get%20keys_list%20%26%20get%20cache_stats.jpeg)

- `/cache_properties` directs to get cache properties page
![Post Set Cache Properties](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/post%20cache_properties.jpeg)
![Post Clear Cache](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/get%20image%20hit%20%26%20post%20clear_cache.jpeg)

- `/cache_stats` directs to get cache stats page
![Get Cache Stats](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/get%20keys_list%20%26%20get%20cache_stats.jpeg)

### Backend API Endpoints (Port 5000)
- `/api/upload` post request to upload key and respective file image
- `/api/list_keys` post request to retrieve a list of keys
- `/api/key/<key_value>` post request to retrieve the fiile image of a respective key

### Memcache API Endpoints (Port 5001)
- `/clear_cache` clear memcache and items
- `/refresh_configuration` refresh memcache configuration
- `/put_into_memcache` put key and image into memcache
- `/get_from_memcache` get key and image from memcache
- `/invalidate_specific_key` delete image and respective key from memcache

## Database
This assignment project uses a local mysql database to store the following database. There are 3 different tables: 1 for the images, 1 for the cache properties, and 1 for cache stats.

### Database Schema
![Database Schema](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/database_schema.jpeg)

## Design Decisions

### Independent Flask Instance for Memcache and Backend
- Decision: The decision was to create 2 independent flask instances, one for the memcache, and one for the backend running on port 5001 and 5000 respectively. 
- Alternative: The alternative is to have 1 flask instance and have the memcache to run within the backend service, the downside of this is that it is a monolith architecture which is difficult with scaling as there are more opportunities to conflict and overwrite the services.
- Reason: The reason why there are 2 independent flask instances is because they can be seen as individual services that a backend could potentially refactor out to be a microservice environment. In the future development, the 2 flask instances can be developed independently without interferring with each other and the 2 flask instances will communicate using HTTP requests.

### Synchronous vs Asynchronous Operations
- Decision: The decision was to go with synchronous operations to communicate between webpages, backend and memcache services. This ensures that every operation is completed before executing the next operation; all operations are executed in series.
- Alternative: The alternative is to consider asynchronous operations to communicate between webpages, backend and memcache services, which could allow the process of requests in parallel.
- Reason: Although, it can be faster to execute asynchronous operations due to the fact that it is in parallel, there is alot more infrastructure cost regarding maintain the order of requests. If asynchronous operations were implemented, and one request fails, then a request queue needs to handle the failed case; whether that is to retry the request again at a later time or revert the other changes made by another request in the same function to maintain proper data accuracy. In doing so, concurrency is also introduced where that can add to the complexity to know which is the latest update. In addition, the cost of implementing asynchronous would introduce multithreading which can be expensive if not properly managed through AWS. With the requirement of this assignment, simple get and put calls for images, it is sufficient to implement a simple synchonous operation to meet the specifications, and therefore synchronous operations was chosen.

### Implement the LRU Algorithm
- Decision: The decision was to implement LRU by storing the timestamp as a file attribute in the memcache; this makes it easier to get the least recently used key in the memcache. It can also reduce the time and space to store the LRU key in the put operation.
- Alternative: The alternative is to store the information in another place in the memcache to store the frequency of the key used.
- Reason: It is easier to see what is the LRU key in memcache if we implemented the alternative. However, if we use the alternative, the process would increase and the capacity limit for the memcache required would increase as well. If we use timestamp to record the usage of the key, it would not only save the space in memcache, but also easier to check the status of the file in the memcache. Therefore, we chose to implement LRU by using the timestamp as an attribute of the file.

## Graphs

### Graph 1 20:80 Read/Write Ratio Latency Graph
### Graph 2 20:80 Read/Write Ratio Throughput Graph
### Graph 3 50:50 Read/Write Ratio Latency Graph
### Graph 4 50:50 Read/Write Ratio Throughput Graph
### Graph 5 80:20 Read/Write Ratio Latency Graph
### Graph 6 80:20 Read/Write Ratio Throughput Graph

## Discussions

## Group Members and Contributions:
- [mrchenliang](https://github.com/mrchenliang)
- [BrianQJN](https://github.com/BrianQJN)
- [Heliali](https://github.com/Heliali)

### Contributions Graph
![Contributions](https://github.com/mrchenliang/ECE1779_Project1/blob/main/static/contributions.png)
