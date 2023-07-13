创建于 2023-03-29
关键词: conda.

```sh
## 创建Python虚拟环境
conda create --name ENV_NAME python=3.9.12

## 激活虚拟环境ENV_NAME
conda activate ENV_NAME

## 退出当前虚拟环境
conda deactivate

## 导出环境配置文件
conda env export -> environment.yml

## 创建环境配置文件
conda env create --file environment.yml

## 所有虚拟环境列表
conda env list

## 删除虚拟环境ENV_NAME
conda env remove --name ENV_NAME
```

