# 需求文档

[TOC]

## 项目背景

## 项目概述

## 需求说明

### 功能需求

#### 启动器

启动器是整个系统的启动入口，提供以下功能：

| 功能 | 参数 | 说明 |
| :-: | :-: | :-- |
| 启动 | run | 启动系统 |
| 停止 | stop | 停止系统 |
| 重启 | restart | 重启系统 |
| 状态 | status | 查询系统状态 |
| 帮助 | help | 显示帮助信息，读取HELP文本文件，并显示其内容 |
| 版本 | version | 读取version属性，显示版本信息 |
| 日志 | log | 显示日志信息 |

   
   启动系统的流程：
1. 输入参数中包含一个PID文件路径。当该文件存在时，其内容为一个PID，表示系统已经启动。此时，启动器会检查该PID对应的进程是否存在，如果存在，则提示系统已经启动，否则删除该PID文件。
2. 如果PID文件不存在，则启动器


#### Scheduler

Scheduler 基于APScheduler实现，提供以下功能：

1. Job以json格式进行管理，包括name, id, time, trigger, task。
2. Job的触发器支持CronTrigger、DateTrigger、IntervalTrigger等。
3. Job的执行器是一个Python函数，Scheduler会调用该函数执行Job。
4. 当执行add_job时，Scheduler会根据Json内容，将Job添加到调度器队列中。
5. 如果json中的name属性已经存在，则执行update_job操作。
6. 以time属性来定义Job的执行时间，并转译为Cron表达式。
7. hh:mm:ss格式, 则定义为每日的该时间执行。
8. hh:mm:ss, mon，tue，wed，thu，fri，sat，sun格式，定义为每周的该时间执行。
9. hh:mm:ss, weekday格式，定义为工作日的该时间执行。
10. hh:mm:ss, weekend格式，定义为周末的该时间执行。
11. hh:mm:ss, day格式，定义为每月的该时间执行。

### 非功能需求

在/opt/quantum/bin下使用source activate 激活虚拟环境，再用pip3安装相关依赖包。
