

[toc]



#### linux 安全检查

查看谁登陆了服务器

```
$ last | more 
```

#### centos 防火墙常用命令

修改完规则，需要重启防火墙

1. 查看防火墙状态

   ```
   firewall-cmd --state
   ```

2. 启动防火墙

   ```
   systemctl start firewalld
   ```

3. 关闭防火墙

   ```
   systemctl stop firewalld
   ```

4. 检查防火墙开放的端口

   ```
   firewall-cmd --permanent --zone=public --list-ports
   ```

5. 开放一个新的端口

   ```
   firewall-cmd --zone=public --add-port=8080/tcp --permanent
   ```

6. 重启防火墙

   ```
   firewall-cmd --reload
   ```

7. 验证新增加端口是否生效

   ```
   firewall-cmd --zone=public --query-port=8080/tcp
   ```

8. 防火墙开机自启动

   ```
   systemctl enable firewalld.service
   ```

9. 取消某一开放端口

   ```
   firewall-cmd --zone=public --remove-port=9200/tcp --permanent
   ```

10. 查看防火墙规则

    ```
    firewall-cmd --list-all
    ```

    
