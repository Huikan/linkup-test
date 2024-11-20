# gossip semantic search engine

This is for linkup exercise.

### System design 
1. Frontend: A web client interacts with a Flask REST API.
2. Backend: 
2.a. Flask communicates with Qdrant for vector search.
2.b. A background job fetches and processes RSS feeds. I used RSS feed source that allows incrementally sniffer the latest news. The only drawback is no rss for full archive available for both sites. 
3 Storage: Qdrant stores vector embeddings and metadata.

### To run the project 
1. build the docker image
```
make build 
```

2. run and run the web service 
```
make service_up
```

3. initialize vector collection `gossip`
```
make init
```

4. fill the vector collection `gossip` with the rss feed
```
make rss_load
```

5. go to the local web UI localhost:5000 to do query test

Here's a [demo](https://www.loom.com/share/de30120f83b049818f7f6e836a423fd5?sid=4d0b16af-90f0-428a-8046-31ac5971b5b5)!

### Further steps we could discuss during our interview: 
1. scalability: 
1.a qdrant is suitable for a local demo. on prod, pinecone could be a good candidate
1.b deploy the app on kubernetes for auto scaling and use a load balancer in front of the flask app
1.c batch fetch rss articles with orchestrator (queue system like celery or rabbitMQ)

2. perfomance: reduce search latency with cach system or light weight in-mem storage 

and of course improve web UI for a better user experience!
