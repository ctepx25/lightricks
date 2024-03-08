## Observability Integration Script

### Build: 
1. Update env vars in Docker file
> ENV OBSERVABILITY_ENDPOINT=""
> 
> ENV CORALOGIX_ENDPOINT=""
> 
> ENV CORALOGIX_SUBSYSTEM_NAME=""
> 
> ENV INFULXDB_ENDPOINT=""
> 
> ENV INFLUXDB_DATABASE=""


2. Build image
> docker build -t \<tag\> .

### Running the script:
1. Make sure to export **coralogix api key** and **influxdb api token** env variables:
>  export CORALOGIX_API_KEY="\**********************"
>  
> export INFLUXDB_API_TOKEN="\**********************"

2. Run the container:
> docker run -it --rm --name \<name\> -e CORALOGIX_API_KEY -e INFLUXDB_API_TOKEN \<tag\>:latest
