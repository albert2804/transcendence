#!/bin/bash

# Wait for Elasticsearch to become healthy
until curl -k -f -u elastic:$ELASTIC_PASSWORD https://elasticsearch:9200; do
	echo "Waiting for Elasticsearch..."
	sleep 1
done

# # Generate an enrollment token
# TOKEN=$(curl -k -f -u elastic:$ELASTIC_PASSWORD -X POST "https://elasticsearch:9200/_security/enroll/node" -H "Content-Type: application/json" -d'{}' | jq -r .token)

# echo "TOKEN: $TOKEN"

# # Use the token to configure Kibana
# echo "xpack.security.enrollmentToken: \"$TOKEN\"" >> /usr/share/kibana/config/kibana.yml

# Start Kibana
exec /usr/local/bin/kibana-docker