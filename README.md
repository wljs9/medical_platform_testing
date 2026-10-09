# 医疗管理平台 · 测试工程

基于 Spring Boot 3 + MyBatis + MySQL 全栈项目(**medical_platform**)的完整接口测试作品集。

> 被测项目支持:科室 / 医生 / 患者 / 病历 / 检查申请 五大模块,53 个 REST 接口。

## 📁 目录结构

```
├── postman/          # 接口功能测试(Postman Collection + Newman)
│   ├── medical-platform.postman_collection.json   # 61 个请求,6 个业务文件夹
│   └── newman-report.html                         # 回归执行报告
├── jmeter/           # 性能测试(命令行模式)
│   ├── 性能测试_查询接口.jmx                       # 压测脚本(3接口 x 100并发)
│   ├── run-performance.bat                          # 一键爬坡执行脚本
│   ├── report_perf_100t_50l/index.html             # 100并发完整报告(1.5万请求,0%错误)
│   └── perf_100t_50l.jtl                           # 原始请求日志
├── pytest/           # 接口自动化测试(分层框架)
│   ├── config.py            # 环境配置层
│   ├── api/                 # 接口封装层(每模块一个文件)
│   ├── testcases/           # 用例层(11条:6过/4预失败/1缺陷)
│   └── report/              # pytest-html 可视化报告
├── defects/          # 缺陷清单(10条,含复现步骤/根因/代码证据)
└── docs/             # 测试总结报告 + 学习指南
```

## ✅ 测试范围与成果

| 测试类型 | 工具 | 规模 | 核心成果 |
|---|---|---|---|
| 接口功能 | Postman + Newman | 61 请求 / 53 接口 | 全量回归,异常场景 8 条 |
| 性能 | JMeter CLI | 1.5 万请求 × 100 并发 | 0% 错误率,瓶颈定位 |
| 自动化 | pytest + requests | 11 条用例 | 6 过 / 4 预失败 / 1 缺陷 |
| 缺陷管理 | — | 10 条(3 P1 / 4 P2 / 1 P3) | 含根因分析与修复建议 |

## 🐛 核心缺陷(亮点)

- **DEF-004**:删除患者未级联子表,外键 `NO ACTION` 拦截 → 500(service 级联代码被注释)
- **DEF-002**:`id_card char(10)` 存不下 18 位身份证 → `Data too long`
- 批量接口无 `@Transactional`,部分成功不回滚(count 79→82)

## 🚀 快速复现

```bash
# 1. 功能回归(需启动被测后端 :8080)
cd postman && newman run medical-platform.postman_collection.json --env-var base_url=http://localhost:8080

# 2. 性能爬坡
cd jmeter && run-performance

# 3. 自动化
cd pytest && python -m pytest testcases/ --html=report/pytest_report.html --self-contained-html
```

> ⚠️ 被测项目的数据库密码已改为环境变量注入(`${DB_PASSWORD}`),不再硬编码于仓库。