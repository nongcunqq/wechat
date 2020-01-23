#### Str, datetime类型互换

起因，从mongodb中导出数据到MySQL中，时间字段导入时报错，发现是MySQL中字段类型为datetime，而导入的是string类型，修改类型后导入成功。

类型转换代码如下：

```python
import time, datetime

t = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
t2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

date_time = datetime.datetime.strptime(t,'%d/%m/%Y %H:%M:%S')
print(t)
print('t type is ', type(t))
print(date_time)
print('date_time type is ', type(date_time))
```

![image-20200115162937275](https://tva1.sinaimg.cn/large/006tNbRwly1gaxbunb9iwj30vw0ihgpe.jpg)