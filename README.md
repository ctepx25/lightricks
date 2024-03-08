## Observability Integration Script

### Build: 
> docker build -t \<tag\> .

### Running the script:
1. Export coralogix api key and influxdb api token variables:
>  export CORALOGIX_API_KEY="\**********************"
> 
> export INFLUXDB_API_TOKEN="\**********************"

2. Run the container:
> docker run -it --rm --name \<name\> -e CORALOGIX_API_KEY -e INFLUXDB_API_TOKEN \<tag\>:latest
