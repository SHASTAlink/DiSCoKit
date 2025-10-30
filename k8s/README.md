# Shade2
## Setup
### Namespace
Run the following command to create the `shade2` namespace in kubernetes:
```bash
kubectl create namespace shade2
```
### Secrets
#### tls certs
this will use self-signed certs to encrypt traffic between app and reverse proxy:

```bash
# generate self-signed cert
openssl genrsa -out tls.key 4096
openssl req -new -x509 -key tls.key -out tls.crt -days 3650

# load tls certs into kubernetes secret
kubectl create secret tls -n shade2 tls-certs --cert=./tls.crt --key=./tls.key
```

#### regcred
used to read images in shade2 project in harbor.ischool.syr.edu:
```bash
kubectl create secret docker-registry regcred -n shade2 --docker-server=harbor.ischool.syr.edu --docker-username='robot$shade2+access' --docker-password=<password>
```

#### app secrets
create a file called `shade2-secret.yaml` and add the following:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: shade2-secret
  namespace: shade2
stringData:
  flask-secret: <string>
  model-subscription-key: <string>
```

then apply the secret to kubernetes:
```bash
kubectl apply -f ./shade2-secret.yaml
```
