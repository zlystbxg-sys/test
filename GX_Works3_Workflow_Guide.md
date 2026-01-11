# GX Works3 PLC开发完整工作流程

## 确认的最佳实践

基于实际测试验证，以下是GX Works3 PLC项目开发的标准化工作流程：

### 第一步：ST程序开发
使用标准化模板开发ST程序，包含详细的中文注释：

```st
// 输入信号定义
Start_Button    : BOOL := FALSE;    // 启动按钮 (X0)
Stop_Button     : BOOL := FALSE;    // 停止按钮 (X1) 
Emergency_Stop  : BOOL := FALSE;    // 急停按钮 (X2) - 常闭触点
```

### 第二步：生成简洁XML文件
使用验证成功的简洁格式生成XML：

```xml
<Variable name="gStart_Button"><Type><TypeName>BOOL</TypeName></Type><Address address="X0" /></Variable>
<Variable name="gStop_Button"><Type><TypeName>BOOL</TypeName></Type><Address address="X1" /></Variable>
<Variable name="gEmergency_Stop"><Type><TypeName>BOOL</TypeName></Type><Address address="X2" /></Variable>
```

**关键要点**：
- 不包含复杂的AddData结构
- 不包含variableComments元素
- 使用与Windsurf样本一致的简洁格式

### 第三步：导入GX Works3
1. 在GX Works3中选择导入IEC 61131-10 XML文件
2. 选择生成的简洁XML文件
3. 确认导入成功，程序和变量正确加载

### 第四步：添加中文注释
在GX Works3的标签编辑器中：
1. 打开全局标签或局部标签编辑器
2. 在注释列中添加中文说明
3. 参考ST程序中的注释内容

或使用CSV文件批量导入（推荐）：
1. 准备全局/局部两个CSV文件（不要混在一个CSV里）
2. 在GX Works3中选择 "工具" → "标签" → "从CSV文件导入"
3. 先导入全局CSV（第1行应为 `"(工程未设置)"`）
4. 再导入局部CSV（第1行应为 `"(ProgramName)"`，例如 `"(Motor_Control)"`）

**CSV导入关键格式（已验证）**：
- 编码：`UTF-16`（带BOM）
- 分隔符：`TAB`
- 每个字段：必须使用英文双引号 `"` 包裹

### 第五步：验证和测试
1. 检查程序逻辑正确性
2. 验证I/O地址分配
3. 测试程序功能

### 第六步：导出完整版本
导出包含中文注释的完整文件：
1. 导出CSV格式 - 包含多语言注释
2. 导出XML格式 - 包含variableComments结构
3. 保存为项目文档

## 文件结构说明

### 开发阶段文件
- `ProjectName.st` - ST源程序（含中文注释）
- `ProjectName_Import.xml` - 用于导入的简洁XML文件

### 完成阶段文件
- `ProjectName.csv` - 导出的CSV文件（含中文注释）
- `ProjectName_Export.xml` - 导出的完整XML文件（含注释结构）
- `ProjectName.gx3` - GX Works3项目文件

## 作为模板使用（推荐）

本仓库可以作为“ST程序 + 一键生成GX Works3可导入文件（XML + 标签CSV）”的模板。

### 1. 准备你的ST程序
1. 复制 `PLC_Program_Template.st` 或参考 `FX5U_Motor_Control.st` 新建一个 `YourProject.st`
2. 在变量行尾使用 `//` 写中文说明
3. 对需要作为全局标签导入的I/O点，在注释中写明地址，例如：`// 启动按钮 (X0)`、`// 电机接触器 (Y0)`

### 2. 生成可导入文件
在本目录执行（PowerShell/CMD均可）：
```bash
python gx_works3_hybrid_generator.py --st-file YourProject.st --output-base YourProject_Import
```

可选：显式指定XML模板（一般不需要）：
```bash
python gx_works3_hybrid_generator.py --st-file YourProject.st --xml-source FX5U_Motor_Control_Windsurf_Format.xml --output-base YourProject_Import
```

生成结果：
- `YourProject_Import.xml`
- `YourProject_Import_Global_Labels.csv`
- `YourProject_Import_Local_Labels.csv`
- `YourProject_Import_Import_Instructions.md`

### 3. 在GX Works3中导入
1. "文件" → "导入" → "IEC 61131-10"：导入 `YourProject_Import.xml`
2. "工具" → "标签" → "从CSV文件导入"：导入 `YourProject_Import_Global_Labels.csv`
3. 再次 "从CSV文件导入"：导入 `YourProject_Import_Local_Labels.csv`

### 4. CSV导入关键规范（已验证）
- 编码：`UTF-16`（带BOM）
- 分隔符：`TAB`
- 每个字段：英文双引号包裹
- 全局/局部：必须分开CSV导入

## 模板文件使用

### 可用模板
1. `PLC_Program_Template.st` - ST程序模板
2. `PLC_Template_XML_Generator.xml` - XML生成模板
3. `FX5U_Motor_Control_Simple_Test.xml` - 验证成功的示例

### 模板定制
根据具体项目需求：
1. 修改变量定义和I/O分配
2. 调整程序逻辑和控制算法
3. 更新中文注释和说明

## 常见问题解决

### XML导入失败
**原因**：XML格式过于复杂或包含不支持的元素
**解决**：使用简洁格式，移除复杂的AddData结构

### 中文注释丢失
**原因**：XML导入时不支持variableComments
**解决**：导入后手动添加，然后导出保存

### 变量地址冲突
**原因**：I/O地址重复分配
**解决**：使用I/O分配表统一管理

## 质量控制检查单

### 导入前检查
- [ ] XML文件格式简洁，无复杂AddData
- [ ] 所有变量类型正确定义
- [ ] I/O地址无冲突
- [ ] 程序逻辑完整

### 导入后检查
- [ ] 所有变量成功导入
- [ ] 程序结构正确
- [ ] I/O地址正确分配
- [ ] 中文注释已添加

### 最终验证
- [ ] 程序编译无错误
- [ ] 功能测试通过
- [ ] 文档完整
- [ ] 版本控制更新

---
*基于GX Works3实际测试验证*  
*版本: V1.0*  
*更新日期: 2026-01-11*
