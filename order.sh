#!/usr/bin/env bash

host="testnet.binance.vision"
# Set up authentication:
apiKey=""
secretKey=""

# Set up the request:
apiMethod="POST"
apiCall="v3/order"
symbol="LTCBTC"
side="SELL"
if $(command -v jq > /dev/null)
then
    price=$(curl -s "https://$host/api/v3/avgPrice?symbol=$symbol" | jq ".price" | sed 's/"//g')
else
    price=$(curl -s "https://$host/api/v3/avgPrice?symbol=$symbol" | sed -E 's/{.*"price":"([0-9]{1,}.[0-9]{2,})".*/\1/g')
fi
apiParams="symbol=$symbol&side=$side&type=LIMIT&timeInForce=GTC&quantity=1&price=$price&recvWindow=5000" 

function rawurlencode {
    local value="$1"
    local len=${#value}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<len ; pos++ ))
    do
        c=${value:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * )   printf -v o '%%%02x' "'$c"
        esac
        encoded+="$o"
    done

    echo "$encoded"
}

ts=$(date +%s000)
paramsWithTs="$apiParams&timestamp=$ts"

rawSignature=$(echo -n "$paramsWithTs" \
               | openssl dgst -sha256 -hmac "$secretKey" \
               | awk '{print $2}')

signature=$(rawurlencode "$rawSignature")

curl --silent -H "X-MBX-APIKEY: $apiKey" -X $apiMethod "https://$host/api/$apiCall?$paramsWithTs&signature=$signature"
