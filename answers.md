**1) We have a k8s cluster in amazon. We need to deploy a new version of my application hub.test.io/app_v1.17b
To minimize possible downtime i select blue-green scheme. Pls describe a deployments example with tag selection.
**

I will consider the app in the task to be very simple because there are no other details about it. Also, I suppose the task is not about the green-blue deployment strategy. And we will assume that there is an ingress balancer that redirects the app’s traffic on the service with “name: app” label.

And, by the way, let's say we have another app “app-green” with another version in this namespace and other “target” and “version” labels. We deploy the “app-blue” nearby because we don’t want to rewrite the green app. And when we will be ready to switch the app’s traffic we should apply the second resource for rewriting the existing service.

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 1
  template:
    metadata:
      labels:
        name: app
        version: "1.17"
        target: blue
spec:
      containers:
        - name: nginx
          image: hub.test.io/app_v1.17b
          ports:
            - name: http
              containerPort: 80
---
apiVersion: v1
kind: Service
metadata: 
  name: app
  labels: 
    name: app
spec:
  ports:
    - name: http
      port: 80
      targetPort: 80
  selector:
    version: "1.17"
    target: blue
    
 ```
    

**2) We have many services in our cluster. How can we prevent infrastructure`s attack (ex DDOS) because we have one ingress with multiple ports?
**

let’s say we have a cluster. it consists of several nodes and each is available for other nodes only via an internal net. We can provide one or several nodes only for ingress and hang out external IP addresses only on that hosts. We deny any traffic by default but open needed particular ports and set up a policy that allows only some kind of traffic for that or another port. "Deny all and allow only what you really need" we can say. In small projects, we can ban IP addresses if they send spam traffic during DDoS attacks. It will defend only in simple cases. I suppose there is a way to filter traffic by myself or we can use some special external tools such as Cloudflare. By the way, I think auto-scale solutions can help you take some more time to resolve the problem and don't lose real users' requests.

3) Check this Dockerfile

```
FROM ubuntu:18.04
COPY ./src /app
RUN apt-get update -y
RUN apt-get install -y nodejs
RUN np_m install
ENTRYPOINT ["npm"]
CMD ["run", "prod"]
```

What's going on here?
How can we optimize this?

 The dockerfile describes an app’s building inside a docker container

/# it takes ubuntu environment from the image

FROM ubuntu:18.04 

/# copies source code in the container
COPY ./src /app 

/#  updates repos for the packets installing
RUN apt-get update -y
RUN apt-get install -y nodejs

/# there is a mistake - “npm” should be. This command installs a package and any packages that it depends on
RUN np_m install

/# The command will start with init of the container. I think should be “node” here
ENTRYPOINT ["npm"] 

/# default arguments for the entrypoint. “Run” is redundant here I think
CMD ["run", "prod"]

We can take an image with all needed environment lighter then ubuntu for building the app -node:16-alpine. 

FROM node:16-alpine
COPY ./src /app

WORKDIR /app
RUN npm install
ENTRYPOINT ["node"]
CMD ["prod"]
