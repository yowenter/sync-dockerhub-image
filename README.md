# sync-dockerhub-image
Distributed Sync from [DockerHub](http://hub.docker.com)  public images to self own registry .





# 同步 镜像 

在 images 目录下, 

`image.list` ,要同步的 library 镜像

`third_party.list`,  第三方镜像 需要同步的镜像.
请注意，为了避免重复，镜像名最好以字母排序

`image_name_convert.list` , dockerhub 非library 镜像 需要同步 到 namespace 的转换 .

**Attention**
如果 第三方镜像没有被转换成目标 `namespace`, 则不会被同步 .


# 如何部署?

`docker-compose -f sync_image.yml up -d `


	


# todo list

* 同步完成后 删除遗留镜像
* 不同 registry 之间迁移镜像
* 监控
* Command Tools







# 如果您要 立刻 同步某个镜像 ？

 `请您务必小心 。在 python cet6.0 水平以上程序员 指导下操作。`

 - step1 
 
 清空 redis 已有任务队列 :  `flushall`       
 查看任务队列：
    `lrange huey.redis.dockerhuey 0 －1`       
 查看出错队列：
     `lrange huey.errors.dockerhuey 0 -1 `
     
   	
   	
   	
- step 2       
在 容器里执行 python shell

```
 python
 >> from sync_main import sync_image_from_dockerhub    
 >> sync_image_from_dockerhub("***")

 ```
 
 
   
   
   
      
 