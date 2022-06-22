# ZGG内置标准库 - time

time提供了常用的时间和日期相关函数和类

## 函数、类详解

### type Time
ZGG的时间类型

<table>
    <tr>
        <th colspan="2">构造函数</th>
    <tr>
    <tr>
        <td>__init__()</td>
        <td>构造一个当前时间的Time对象</td>
    </tr>
    <tr>
        <td>__init__(goTime)</td>
        <td>根据传入的go的time.Time值，生成一个zgg的Time对象</td>
    </tr>
    <tr>
        <td>__init__(unixNano)</td>
        <td>构造一个单位为纳秒的时间戳为unixNano的Time对象，时区为机器当前时区</td>
    </tr>
    <tr>
        <td>__init__(timeStr)</td>
        <td>
            将timeStr解析为Time对象。支持以下格式的字符串（下面以go的时间格式表达方法说明）：
            <ul>
                <li>20060102</li>
                <li>2006-01-02</li>
                <li>20060102150405</li>
                <li>2006-01-02 15:04:05</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>__init__(timeStr, layout)</td>
        <td>按layout格式将timeStr解析为Time对象。layout的格式为go的时间layout格式</td>
    </tr>
    <tr>
        <td>__init__(year, month, day)</td>
        <td>
            生成一个时间为当前时区的year年month月day日0时0分0秒的Time对象
        </td>
    </tr>
    <tr>
        <td>__init__(year, month, day, hour, minute, second)</td>
        <td>
            生成一个时间为当前时区的year年month月day日hour时minute分second秒的Time对象
        </td>
    </tr>
    <tr>
        <th colspan="2">对象属性（只读）</th>
    <tr>
    <tr>
        <td>unix</td>
        <td>Time对象对应的unix时间戳（精确到秒）。Int</td>
    </tr>
    <tr>
        <td>unixNano</td>
        <td>Time对象对应的unix时间戳（精确到纳秒）。Int</td>
    </tr>
    <tr>
        <td>year</td>
        <td>Time对象对应的年份。Int</td>
    </tr>
    <tr>
        <td>month</td>
        <td>Time对象对应的月份(1~12)。Int</td>
    </tr>
    <tr>
        <td>day</td>
        <td>Time对象对应的日期(1~31)。Int</td>
    </tr>
    <tr>
        <td>hour</td>
        <td>Time对象对应的小时(0~23)。Int</td>
    </tr>
    <tr>
        <td>minute</td>
        <td>Time对象对应的分钟(0~59)。Int</td>
    </tr>
    <tr>
        <td>second</td>
        <td>Time对象对应的秒(0~59)。Int</td>
    </tr>
    <tr>
        <th colspan="2">方法</th>
    <tr>
    <tr>
        <td>add(durationStr)</td>
        <td>返回一个新的Time对象，其取值为当前Time对象加上duration。<br/>duration的值为go语言的duration表达字符串</td>
    </tr>
    <tr>
        <td>addDays(daysInt)</td>
        <td>返回一个新的Time对象，其取值为当前Time对象加daysInt天</td>
    </tr>
    <tr>
        <td>addHours(hoursInt)</td>
        <td>返回一个新的Time对象，其取值为当前Time对象加hoursInt个小时</td>
    </tr>
    <tr>
        <td>format(layout)</td>
        <td>将Time对象格式化为一个字符串。layout的格式与go语言一致</td>
    </tr>
    <tr>
        <td>timetuple</td>
        <td>返回Time对象对应的[year, month, day, hour, minute, second, location]</td>
    </tr>
    <tr>
        <td>toGoTime</td>
        <td>根据该Time对象，返回一个对应的go语言的time.Time值</td>
    </tr>
</table>

### func time()
返回当前的unix时间戳，精确到秒。等同于```Time().unix```

### func now
```TODO```

### func fromUnix(timestamp)
根据传入的unix时间戳（精确到秒）返回Time对象。等同于```Time(timestamp * 1000000000)```

### func fromGoTime(goTime)
根据传入的go的time.Time值，生成一个zgg的Time对象

### func sleep(secondsFloat)
当前线程暂停secondsFloat秒

### func timeit(callable)
运行callable，返回耗时，单位为纳秒
