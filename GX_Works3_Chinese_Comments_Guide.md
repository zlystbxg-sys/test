# GX Works3 中文注释完整指南

## 重要发现

通过分析用户导出的`Motor_Control.csv`和`Motor_Control.xml`文件，发现了GX Works3处理中文注释的正确方法。

## CSV格式中的中文注释

GX Works3的CSV导出格式支持多语言注释系统：

```csv
"类"	"标签名"	"数据类型"	...	"Chinese Simplified/简体中文"	...
"VAR"	"Motor_Run_Command"	"BOOL"	...	"电机运行命令"	...
```

**特点**:
- 中文注释存储在`"Chinese Simplified/简体中文"`列
- 支持多种语言的注释
- 可以直接编辑CSV文件添加中文注释

## CSV导入格式关键规范（已验证可导入）

以下规范以`Motor_Control_test1.csv`（从GX Works3导出并验证可正常导入）为准：

- **编码**: `UTF-16`（带BOM）
- **分隔符**: `TAB`（制表符），不是逗号
- **引号规则**: 每个字段都用英文双引号 `"` 包裹
- **作用域分离**:
  - **全局标签CSV**: 第1行必须是 `"(工程未设置)"`
  - **局部标签CSV**: 第1行必须是 `"(ProgramName)"`，例如 `"(Motor_Control)"`
  - 全局/局部不要混在同一个CSV里导入
- **变量名匹配**:
  - CSV中的`"标签名"`必须与GX Works3当前工程中的标签名一致
  - 例如XML里全局变量是`gStart_Button`，CSV也必须使用`gStart_Button`，不能用`Start_Button`

### 推荐工作方式

使用仓库中的生成器输出可直接导入的标签CSV：
- 全局: `*_Global_Labels.csv`
- 局部: `*_Local_Labels.csv`

这些文件会按上述规范生成（UTF-16 + TAB + 全字段引号），适合直接在GX Works3中“从CSV文件导入”。

## XML格式中的正确中文注释结构

### 发现的正确格式

```xml
<variable name="Motor_Run_Command" address="LV:0.0">
  <type><BOOL /></type>
  <addData>
    <data name="http://www.mitsubishielectric.com/xml/variableComments" handleUnknown="implementation">
      <variableComments>
        <comment number="8">
          <html xml:space="preserve" xmlns="http://www.w3.org/1999/xhtml">电机运行命令</html>
        </comment>
      </variableComments>
    </data>
  </addData>
</variable>
```

### 关键要素分析

1. **专有命名空间**: `http://www.mitsubishielectric.com/xml/variableComments`
2. **HTML包装**: 注释内容必须包装在`<html>`标签中
3. **空格保留**: 必须使用`xml:space="preserve"`属性
4. **注释编号**: 每个注释需要唯一的`number`属性
5. **XHTML命名空间**: `xmlns="http://www.w3.org/1999/xhtml"`

## 在IEC 61131-10 XML中应用

### 全局变量的中文注释

```xml
<Variable name="gStart_Button">
  <Type><TypeName>BOOL</TypeName></Type>
  <Address address="X0" />
  <AddData>
    <Data name="http://www.mitsubishielectric.com/xml/variableComments" handleUnknown="implementation">
      <variableComments>
        <comment number="10">
          <html xml:space="preserve" xmlns="http://www.w3.org/1999/xhtml">启动按钮 (X0)</html>
        </comment>
      </variableComments>
    </Data>
  </AddData>
</Variable>
```

### 局部变量的中文注释

```xml
<Variable name="Motor_Run_Command">
  <Type><TypeName>BOOL</TypeName></Type>
  <AddData>
    <Data name="http://www.mitsubishielectric.com/xml/variableComments" handleUnknown="implementation">
      <variableComments>
        <comment number="1">
          <html xml:space="preserve" xmlns="http://www.w3.org/1999/xhtml">电机运行命令</html>
        </comment>
      </variableComments>
    </Data>
  </AddData>
</Variable>
```

## 注释编号管理

### 编号规则建议

- **局部变量**: 1-99
- **全局输入**: 100-199  
- **全局输出**: 200-299
- **参数变量**: 300-399
- **系统变量**: 400-499

### 示例编号分配

```xml
<!-- 局部变量 -->
<comment number="1">电机运行命令</comment>
<comment number="2">保护条件正常</comment>

<!-- 全局输入 -->
<comment number="100">启动按钮 (X0)</comment>
<comment number="101">停止按钮 (X1)</comment>

<!-- 全局输出 -->
<comment number="200">电机接触器 (Y0)</comment>
<comment number="201">运行指示灯 (Y1)</comment>
```

## 实际应用示例

### 完整的变量定义（带中文注释）

```xml
<Variable name="gEmergency_Stop">
  <Type><TypeName>BOOL</TypeName></Type>
  <Address address="X2" />
  <AddData>
    <Data name="http://www.mitsubishielectric.com/xml/variableComments" handleUnknown="implementation">
      <variableComments>
        <comment number="102">
          <html xml:space="preserve" xmlns="http://www.w3.org/1999/xhtml">急停按钮 (X2) - 常闭触点</html>
        </comment>
      </variableComments>
    </Data>
  </AddData>
</Variable>
```

## 常见错误和解决方案

### ❌ 错误格式1: 使用Documentation元素
```xml
<!-- 这种格式会导致导入失败 -->
<Documentation>
  <xhtml xmlns="http://www.w3.org/1999/xhtml">中文注释</xhtml>
</Documentation>
```

### ❌ 错误格式2: 缺少HTML包装
```xml
<!-- 这种格式不会显示注释 -->
<variableComments>
  <comment number="1">中文注释</comment>
</variableComments>
```

### ✅ 正确格式
```xml
<Data name="http://www.mitsubishielectric.com/xml/variableComments" handleUnknown="implementation">
  <variableComments>
    <comment number="1">
      <html xml:space="preserve" xmlns="http://www.w3.org/1999/xhtml">中文注释</html>
    </comment>
  </variableComments>
</Data>
```

## 最佳实践建议

### 1. 注释内容规范
- 简洁明了，描述变量用途
- 包含I/O地址信息
- 标明触点类型（常开/常闭）
- 使用统一的描述格式

### 2. 编号管理
- 预先规划编号范围
- 保持编号的唯一性
- 按功能分组编号
- 预留扩展空间

### 3. 模板化应用
- 创建标准的注释模板
- 统一变量命名和注释格式
- 建立项目级的注释规范

## 工具和流程

### 开发流程
1. **编写ST程序** - 包含详细注释
2. **生成XML文件** - 使用正确的variableComments格式
3. **导入GX Works3** - 验证注释显示正确
4. **导出验证** - 检查CSV和XML导出结果

### 验证方法
1. 导入XML文件到GX Works3
2. 检查标签编辑器中的注释显示
3. 导出CSV文件验证中文注释
4. 导出XML文件确认格式正确

---
*基于实际GX Works3导出文件分析*  
*版本: V1.0*  
*更新日期: 2026-01-11*
