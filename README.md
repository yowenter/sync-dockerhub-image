# sync-dockerhub-image
Distributed Sync docker hub (or other registry) public images to third party registry .




# 同步 镜像 

在 images 目录下, 

`image.list` ,要同步的 library 镜像

`third_party.list`,  第三方镜像 需要同步的镜像

`image_name_convert.list` , dockerhub 非library 镜像 需要同步 到 namespace 的转换 .

**Attention**
如果 第三方镜像没有被转换成目标 namespace, 则不会被同步 .