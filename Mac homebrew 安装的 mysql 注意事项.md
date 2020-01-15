#### Mac homebrew 安装的 mysql 注意事项

查询my.conf 配置文件位置

```
mysql --verbose --help | grep my.cnf
/etc/my.cnf /etc/mysql/my.cnf /usr/local/etc/my.cnf ~/.my.cnf 
```

![image-20200115150227643](https://tva1.sinaimg.cn/large/006tNbRwly1gax9c5315uj30ty0e6q3t.jpg)

##### Mysql ERROR 1067: Invalid default value for 字段

永久解决：
在 my.cnf 文件中添加如下配置

```
sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

#### 设置 mysql 开机启动

在终端输入

```
sudo vi /Library/LaunchDaemons/com.mysql.mysql.plist  
```

输入启动文件内容

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>KeepAlive</key>
    <true/>
    <key>Label</key>
    <string>com.mysql.mysqld</string>
    <key>ProgramArguments</key>
    <array>
    <string>/usr/local/Cellar/mysql/8.0.11/bin/mysqld_safe</string>    
    <string>--user=root</string>
    </array>
  </dict>
</plist>

```

/usr/local/Cellar/mysql/8.0.11/bin/mysqld_safe 是mysql_safe的路径

加载启动文件，终端里输入：

```
sudo launchctl load -w /Library/LaunchDaemons/com.mysql.mysql.plist  
```

查看下MySQL是否启动

```
ps -aef | grep mysql
```

