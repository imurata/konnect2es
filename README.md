## What's this?

Transfer Konnect Audit Logs to Elasticsearch.

## How to use
0. Clone Repository

1. Make a container image & push to the repository.
```
MYREPO=myrepo/konnect2es
docker build --platform linux/amd64 -t $MYREPO .
docker push $MYREPO
```

2. Edit K8s Manifest.
- Image Name
- Hostname for Ingress
- Email for Issuer

3. Edit K8s Secret to connect ES.

4. Run.
```
kubectl apply -f ./k8s
```

5. Modify Konnect Audit settings.
For cli. (Of course, you can update it from the UI.)
```
http PATCH https://global.api.konghq.com/v2/audit-log-webhook \
    Content-Type:application/json \
    Authorization:"Bearer $KONNECT_TOKEN" \
    endpoint="https://${ELASTIC_HOST}/konnect/_doc" \
    enabled:=true \
    skip_ssl_verification:=true \
    authorization="" \
    log_format="json"
```


