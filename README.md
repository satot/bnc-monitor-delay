# How to run

1. Obtain API Key and Secret Key from https://testnet.binance.vision/key/generate
2. Paste the API Key and Secret Key onto `get_listen_key.sh` and `order.sh`
3. Run following commands to obtain listen key

```
$ bash get_listen_key.sh
```

4. Run following commands to start monitor process; The app will ask to key in delay and listen key

```
$ docker build scripts/ -t satot/ws-monitor
$ docker run --name monitor --rm -i satot/ws-monitor python3 client.py
```

5. Order crypto by `order.sh` or some other way. Message will show up when the delay exceeds the value configured by user.

