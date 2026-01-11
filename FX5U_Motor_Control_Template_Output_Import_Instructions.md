# GX Works3 混合导入方案说明

## 生成的文件
- 程序XML文件: FX5U_Motor_Control_Template_Output.xml
- 全局标签CSV: FX5U_Motor_Control_Template_Output_Global_Labels.csv
- 局部标签CSV: FX5U_Motor_Control_Template_Output_Local_Labels.csv

## 完美的导入流程

### 步骤1: 导入程序结构
1. 打开GX Works3
2. 选择 "文件" -> "导入" -> "IEC 61131-10 XML文件"
3. 选择 FX5U_Motor_Control_Template_Output.xml
4. 确认导入，程序结构和逻辑将被导入

### 步骤2: 导入全局标签注释
1. 在GX Works3中，选择 "工具" -> "标签" -> "从CSV文件导入"
2. 选择 FX5U_Motor_Control_Template_Output_Global_Labels.csv
3. 确认导入设置，全局标签的中文注释将被添加

### 步骤3: 导入局部标签注释
1. 选择 "工具" -> "标签" -> "从CSV文件导入"
2. 选择 FX5U_Motor_Control_Template_Output_Local_Labels.csv
3. 确认导入设置，局部标签的中文注释将被添加

## 方案优势

✅ **完全自动化** - 一键生成所有必需文件
✅ **格式兼容** - XML和CSV都使用GX Works3原生支持的格式
✅ **注释完整** - 所有中文注释都能正确显示
✅ **结构清晰** - 全局和局部标签分离管理
✅ **可重复使用** - 适用于所有未来项目

## 验证步骤

1. **检查程序逻辑** - 确认所有程序块和变量正确导入
2. **验证全局标签** - 检查全局标签的地址和注释
3. **验证局部标签** - 检查局部标签的注释显示
4. **测试编译** - 确保程序能正常编译和运行

## 故障排除

### 如果XML导入失败
- 检查XML文件格式是否正确
- 确认GX Works3版本支持IEC 61131-10格式

### 如果CSV导入失败
- 检查CSV文件编码（必须为UTF-16，带BOM）
- 确认CSV分隔符为TAB（制表符），不是逗号
- 确认每个字段都使用英文双引号包裹
- 全局/局部标签CSV必须分开导入：
  - 全局CSV第1行应为"(工程未设置)"
  - 局部CSV第1行应为"(ProgramName)"，例如"(Motor_Control)"
- 检查标签名是否与XML中的变量名匹配

### 如果注释显示异常
- 确认CSV文件中的中文注释在正确的列（Chinese Simplified/简体中文）
- 检查文件编码是否正确

---
*这是目前最完美的GX Works3中文注释自动化解决方案*
*版本: V2.0 混合方案*
*日期: 2026-01-11*
