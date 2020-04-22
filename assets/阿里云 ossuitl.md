阿里云 ossuitl

官方文档，上传下载 cp

[](https://help.aliyun.com/document_detail/120057.html?spm=a2c4g.11186623.2.19.65d31c7aJhHIhc#concept-303810)



本地文档去重上传，cd到根目录下，执行

```
ossutilmac64 cp -r  /Users/a1/Desktop/Jd oss://ljfilestation/Jd/ -u
```

**cp**命令用于上传、下载、拷贝文件。

-r 使用**cp**命令时增加**-r**选项可以将目标文件夹上传到OSS

/Users/a1/Desktop/Jd 本地文件夹目录

oss://ljfilestation/Jd/ 远程文件夹目录

-u 如果有文件则跳过，不跳目录

