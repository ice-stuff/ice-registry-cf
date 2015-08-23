# iCE Registry server - Cloud Foundry deployment

To deploy you need to have a MongoDB service named `ice_mongodb`:

```console
$> cf services
[...]

name          service    plan      bound apps     last operation   
ice_mongodb   mongolab   sandbox   ice_registry   create succeeded   

$> cf push
[...]

urls: ice-registry.cfapps.io
last uploaded: Sun Aug 23 21:04:18 UTC 2015
stack: cflinuxfs2
buildpack: Python

     state     since                    cpu    memory          disk             details
#0   running   2015-08-23 10:05:03 PM   0.0%   66.9M of 128M   144.4M of 256M
```

