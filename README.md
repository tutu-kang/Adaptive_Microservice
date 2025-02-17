# Robust Resource Scaling of Containerized Microservices with Probabilistic Machine learning

Large-scale web services are increasingly being built with many small modular components (microservices), which can be deployed, updated and scaled seamlessly. These microservices are packaged to run in a lightweight isolated execution environment (containers) and deployed on computing resources rented from cloud providers. However, the complex interactions and the contention of shared hardware resources in cloud data centers pose significant challenges in managing web service performance. In this paper, we present RScale, a robust resource scaling system that provides end-to-end performance guarantee for containerized microservices deployed in the cloud. RScale employs a probabilistic machine learning-based performance model, which can quickly adapt to changing system dynamics and directly provide confidence bounds in the predictions with minimal overhead. It leverages multi-layered data collected from container-level resource usage metrics and virtual machine-level hardware performance counter metrics to capture changing resource demands in the presence of multi-tenant performance interference. We implemented and evaluated RScale on NSF Cloud's Chameleon testbed using KVM for virtualization, Docker Engine for containerization and Kubernetes for container orchestration. Experimental results with an open-source microservices benchmark, Robot Shop, demonstrate the superior prediction accuracy and adaptiveness of our modeling approach compared to popular machine learning techniques. RScale meets the performance SLO (service-level-objective) targets for various microservice workflows even in the presence of multi-tenant performance interference and changing system dynamics.

## If you use the code, please cite:
```
@INPROCEEDINGS{
Kang2020UCC,  
author={Kang, Peng and Lama, Palden},  
booktitle={2020 IEEE/ACM 13th International Conference on Utility and Cloud Computing (UCC)},  
title={Robust Resource Scaling of Containerized Microservices with Probabilistic Machine learning},   
year={2020},  
volume={}, 
number={},  
pages={122-131},  
doi={10.1109/UCC48980.2020.00031}}
```

## runtine environment
python3.6

## build robot-shop application.

Go into k8s-robot-shop-application. and install it. 

install helm https://helm.sh/docs/intro/install/

helm version is 3.5.4

k8s version is 1.18.2

## workload

Go into load-gen. and check README.

this ip address is the api to access  the Robot-shop application. 
```
kubectl get service -n robot-shop
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)              AGE
web         ClusterIP   10.105.207.202   <none>        8080/TCP             10d
```
```
locust --host http://`kubectl get service -n robot-shop |grep web| awk '{print $3}'`:8080 -f load-gen/robot-shop.py -u 10 -r 5 -t 60s --print-stats --csv=locust  --headless --stop-time=2
```


## how to run program
```
# online version
cd run
bash run_online.sh
```

```
## collectin training data 
cd run
bash run_offline.sh
```


## how to analyze data

```
cd analyze_data
python driver_main.py ../example_data/
```


## how to solve some error.

## check log
```
kubectl -n robot-shop logs -f container-name
```

erro1: mysql and mongodb
if you are running multiple mysql and mongodb, make sure each pod successfully run.

error2: web only can have 1. if you have mutiple web pod, maybe you will face some 504 errro.


error3: payment error. 
check dispatch can access rabbitmq. If can't, delete pod and create again. 

payment gatway can't access.  check k8s/helm/values.yaml ping payment\_gatway.

error4: cart error. check web's number. and check instana is running successful. 


