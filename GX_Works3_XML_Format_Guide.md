# GX Works3 XML格式完整指南

## 概述

本文档基于对Windsurf生成的可导入XML文件的分析，总结了GX Works3 IEC 61131-10 XML格式的关键要求和最佳实践。

## 关键格式差异对比

### ❌ 错误格式 (PLCopen TC6)
```xml
<?xml version="1.0" encoding="UTF-16"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0201">
```

### ✅ 正确格式 (IEC 61131-10)
```xml
<?xml version="1.0" encoding="utf-8"?>
<Project xmlns="www.iec.ch/public/TC65SC65BWG7TF10" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         schemaVersion="1.000" 
         xsi:schemaLocation="www.iec.ch/public/TC65SC65BWG7TF10 GXW3_IEC61131_10_Ed1_0_ForGXW3.xsd">
```

## XML结构层次

```
Project
├── FileHeader
├── ContentHeader
├── Types
│   └── GlobalNamespace
│       ├── AddData (FbFiles)
│       ├── FunctionBlock (可选)
│       └── Program
└── Instances
    └── Configuration
        ├── Resource
        │   ├── AddData
        │   └── ProgramInstance
        └── GlobalVars (多个组)
```

## 必需元素详解

### 1. 文件头部
```xml
<FileHeader companyName="MITSUBISHI ELECTRIC CORPORATION" 
            companyURL="http://www.mitsubishielectric.com" 
            productName="GX Works3" 
            productVersion="ver.1.0" />
```

### 2. 内容头部
```xml
<ContentHeader name="项目名称" 
               creationDateTime="2026-01-11T15:12:00+10:00" 
               modificationDateTime="2026-01-11T15:12:01+10:00" />
```

### 3. 程序定义
```xml
<Program name="程序名称">
  <AddData>
    <Data name="http://www.mitsubishielectric.com/xml/PouProperties" handleUnknown="implementation">
      <PouProperties title="程序名称" version="ver.1.000" helpFilePath="" supportVersion="1.000W" />
    </Data>
  </AddData>
  
  <Vars constant="false" accessSpecifier="private">
    <Variable name="变量名"><Type><TypeName>BOOL</TypeName></Type></Variable>
  </Vars>
  
  <MainBody>
    <BodyContent xsi:type="ST">
      <ST>
        (* ST代码内容 *)
      </ST>
    </BodyContent>
  </MainBody>
</Program>
```

### 4. 全局变量定义
```xml
<GlobalVars constant="false">
  <AddData>
    <Data name="http://www.mitsubishielectric.com/xml/GlobalVarsProperties" handleUnknown="implementation">
      <GlobalVarsProperties name="组名" title="组名" version="ver.1.000" helpFilePath="" supportVersion="1.000W" />
    </Data>
  </AddData>
  
  <Variable name="变量名">
    <Type><TypeName>BOOL</TypeName></Type>
    <Address address="X0" />
  </Variable>
</GlobalVars>
```

## 数据类型支持

| IEC类型 | XML表示 | 示例 |
|---------|---------|------|
| BOOL | `<TypeName>BOOL</TypeName>` | 开关量 |
| INT | `<TypeName>INT</TypeName>` | 整数 |
| TIME | `<TypeName>TIME</TypeName>` | 时间 |
| TON | `<TypeName>TON</TypeName>` | 定时器 |

## 地址映射规则

### 输入输出地址
- 输入: `X0`, `X1`, `X2`, ...
- 输出: `Y0`, `Y1`, `Y2`, ...
- 内部继电器: `M0`, `M1`, ...
- 数据寄存器: `R100`, `R102`, ...

### 初始值设定
```xml
<Variable name="变量名">
  <Type><TypeName>BOOL</TypeName></Type>
  <InitialValue><SimpleValue value="TRUE" /></InitialValue>
  <Address address="M0" />
</Variable>
```

## 常见错误和解决方案

### 1. 编码问题
❌ `encoding="UTF-16"`
✅ `encoding="utf-8"`

### 2. 命名空间错误
❌ `xmlns="http://www.plcopen.org/xml/tc6_0201"`
✅ `xmlns="www.iec.ch/public/TC65SC65BWG7TF10"`

### 3. 元素大小写
❌ `<project>`, `<program>`
✅ `<Project>`, `<Program>`

### 4. 缺少必需的AddData
每个Program和GlobalVars都必须包含相应的AddData元素

## 最佳实践

1. **使用Windsurf生成**: 最可靠的方法是使用Windsurf直接生成XML
2. **分组管理**: 将相关的全局变量分组到不同的GlobalVars块
3. **地址规划**: 合理规划I/O地址，避免冲突
4. **注释完整**: 在ST代码中添加详细注释
5. **版本控制**: 维护version和modificationDateTime信息

## 导入步骤

1. 在GX Works3中选择"文件" → "导入"
2. 选择"IEC 61131-10"格式
3. 选择XML文件
4. 确认导入设置
5. 检查导入结果

## 故障排除

如果导入失败：
1. 检查XML格式是否符合IEC 61131-10标准
2. 验证命名空间和编码设置
3. 确认所有必需的AddData元素存在
4. 检查变量名和地址是否有冲突
5. 使用XML验证工具检查语法错误

---
*文档版本: V1.0*  
*更新日期: 2026-01-11*  
*基于: GX Works3 ver.1.120A*
