#!/usr/bin/env bash

host="testnet.binance.vision"
# Set up authentication:
apiKey=""

# Set up the request:
apiMethod="POST"
apiCall="v3/userDataStream"

listenKey=$(curl -s -H "X-MBX-APIKEY: $apiKey" -X $apiMethod "https://$host/api/$apiCall" | jq ".listenKey" | sed 's/"//g')
echo $listenKey
