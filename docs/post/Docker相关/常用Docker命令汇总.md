创建于 2022-10-31<br>
关键词: Docker.

```sh
## 启动docker服务
systemctl start docker

## 重启docker服务
systemctl restart docker

## 查看当前所有正在运行的容器
docker ps

## 查看当前所有容器(包括正在运行的和停止运行的容器)
docker ps -a

## 查看所有镜像
docker images

## 关闭正在运行的容器
docker stop CONTAINER_NAME

## 删除停止运行的容器
docker rm CONTAINER_NAME

## 删除镜像
docker rmi IMAGE_NAME

## 启动已停止运行的容器
docker start CONTAINER_NAME

## 重启正在运行的容器
docker restart CONTAINER_NAME

## 启动所有已停止的容器
docker start $(docker ps -aq)

## 提交容器生成镜像
docker commit CONTAINER_NAME REPO:TAG  
## 例：docker commit mypython
```

