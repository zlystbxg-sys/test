(*
================================================================================
FX5U PLC 电机控制程序 (ST语言)
功能: 电机启动/停止控制，带保护功能和状态指示
作者: PLC程序
日期: 2026-01-11
版本: V1.0
================================================================================
*)

PROGRAM Motor_Control
VAR
    // 输入信号定义
    Start_Button    : BOOL := FALSE;    // 启动按钮 (X0)
    Stop_Button     : BOOL := FALSE;    // 停止按钮 (X1) 
    Emergency_Stop  : BOOL := FALSE;    // 急停按钮 (X2) - 常闭触点
    Overload_Relay  : BOOL := FALSE;    // 过载继电器 (X3) - 常闭触点
    Thermal_Switch  : BOOL := FALSE;    // 热保护开关 (X4) - 常闭触点
    Motor_Feedback  : BOOL := FALSE;    // 电机运行反馈 (X5)
    
    // 输出信号定义
    Motor_Contactor : BOOL := FALSE;    // 电机接触器 (Y0)
    Run_Indicator   : BOOL := FALSE;    // 运行指示灯 (Y1) - 绿灯
    Fault_Indicator : BOOL := FALSE;    // 故障指示灯 (Y2) - 红灯
    Ready_Indicator : BOOL := FALSE;    // 就绪指示灯 (Y3) - 黄灯
    
    // 内部变量
    Motor_Run_Command   : BOOL := FALSE;    // 电机运行命令
    Protection_OK       : BOOL := FALSE;    // 保护条件正常
    Start_Condition     : BOOL := FALSE;    // 启动条件
    Stop_Condition      : BOOL := FALSE;    // 停止条件
    Fault_Status        : BOOL := FALSE;    // 故障状态
    
    // 定时器变量
    Start_Delay_Timer   : TON;              // 启动延时定时器
    Fault_Reset_Timer   : TON;              // 故障复位定时器
    
    // 定时器时间常数
    START_DELAY_TIME    : TIME := T#500ms;  // 启动延时时间
    FAULT_RESET_TIME    : TIME := T#3s;     // 故障复位时间
END_VAR

BEGIN
    // ========== 保护条件检查 ==========
    // 检查所有保护输入（常闭触点，正常时为TRUE）
    Protection_OK := Emergency_Stop AND Overload_Relay AND Thermal_Switch;
    
    // ========== 故障检测 ==========
    // 故障条件：任一保护条件不满足
    Fault_Status := NOT Protection_OK;
    
    // ========== 启动条件判断 ==========
    // 启动条件：按下启动按钮 且 保护正常 且 无故障状态
    Start_Condition := Start_Button AND Protection_OK AND NOT Fault_Status;
    
    // ========== 停止条件判断 ==========
    // 停止条件：按下停止按钮 或 出现故障
    Stop_Condition := Stop_Button OR Fault_Status;
    
    // ========== 电机控制逻辑 ==========
    // 启动延时定时器
    Start_Delay_Timer(
        IN := Start_Condition AND NOT Motor_Run_Command,
        PT := START_DELAY_TIME
    );
    
    // 电机运行命令 - 自保持逻辑
    IF Start_Delay_Timer.Q THEN
        Motor_Run_Command := TRUE;
    ELSIF Stop_Condition THEN
        Motor_Run_Command := FALSE;
    END_IF;
    
    // 电机接触器输出
    Motor_Contactor := Motor_Run_Command AND Protection_OK;
    
    // ========== 故障复位逻辑 ==========
    // 故障复位定时器 - 故障消除后自动复位
    Fault_Reset_Timer(
        IN := Protection_OK AND Fault_Status,
        PT := FAULT_RESET_TIME
    );
    
    // 故障状态复位
    IF Fault_Reset_Timer.Q THEN
        Fault_Status := FALSE;
    END_IF;
    
    // ========== 状态指示灯控制 ==========
    
    // 就绪指示灯（黄灯）- 系统正常但电机未运行
    Ready_Indicator := Protection_OK AND NOT Motor_Run_Command AND NOT Fault_Status;
    
    // 运行指示灯（绿灯）- 电机正在运行
    Run_Indicator := Motor_Contactor AND Motor_Feedback;
    
    // 故障指示灯（红灯）- 系统故障
    Fault_Indicator := Fault_Status;
    
END_PROGRAM

(*
================================================================================
I/O 分配表:
================================================================================
输入 (X):
X0 - Start_Button      启动按钮 (常开)
X1 - Stop_Button       停止按钮 (常开) 
X2 - Emergency_Stop    急停按钮 (常闭)
X3 - Overload_Relay    过载继电器 (常闭)
X4 - Thermal_Switch    热保护开关 (常闭)
X5 - Motor_Feedback    电机运行反馈 (常开)

输出 (Y):
Y0 - Motor_Contactor   电机接触器
Y1 - Run_Indicator     运行指示灯 (绿灯)
Y2 - Fault_Indicator   故障指示灯 (红灯)  
Y3 - Ready_Indicator   就绪指示灯 (黄灯)

================================================================================
功能说明:
================================================================================
1. 启动功能:
   - 按下启动按钮，系统检查保护条件
   - 保护正常时，延时500ms后启动电机
   - 电机启动后自保持运行

2. 停止功能:
   - 按下停止按钮立即停止电机
   - 任何保护条件触发时自动停止

3. 保护功能:
   - 急停保护：急停按钮按下时立即停止
   - 过载保护：过载继电器动作时停止电机
   - 热保护：热保护开关动作时停止电机
   - 故障自动复位：故障消除3秒后自动复位

4. 状态指示:
   - 黄灯：系统就绪，可以启动
   - 绿灯：电机正常运行
   - 红灯：系统故障

================================================================================
使用说明:
================================================================================
1. 将此程序下载到FX5U PLC中
2. 按照I/O分配表连接外部设备
3. 确保所有保护设备正常连接
4. 上电后观察指示灯状态
5. 按启动按钮启动电机，按停止按钮停止电机

注意事项:
- 急停、过载、热保护均为常闭触点
- 电机反馈信号用于确认电机实际运行状态
- 故障时红灯亮，故障消除后会自动复位
================================================================================
*)
