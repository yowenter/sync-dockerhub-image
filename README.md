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
