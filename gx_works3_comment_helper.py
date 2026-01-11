#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GX Works3 注释助手工具
提供多种方式来提高注释添加效率

作者: PLC开发助手
版本: V1.0
日期: 2026-01-11
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

class CommentHelper:
    """注释助手主类"""
    
    def __init__(self):
        self.comments = {}
        self.current_file = None
    
    def parse_st_comments(self, st_file_path: str) -> Dict[str, str]:
        """从ST文件中解析变量注释"""
        comments = {}
        
        try:
            with open(st_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配变量定义和注释的正则表达式
            pattern = r'(\w+)\s*:\s*\w+.*?//\s*(.+?)(?:\n|$)'
            matches = re.findall(pattern, content, re.MULTILINE)
            
            for var_name, comment in matches:
                clean_comment = comment.strip()
                if clean_comment:
                    comments[var_name] = clean_comment
            
            return comments
            
        except Exception as e:
            print(f"解析ST文件时出错: {e}")
            return {}
    
    def generate_comment_list(self, st_file_path: str, output_path: str):
        """生成注释清单文件，便于复制粘贴"""
        comments = self.parse_st_comments(st_file_path)
        
        if not comments:
            print("未找到任何注释")
            return
        
        # 生成格式化的注释清单
        content = f"""# GX Works3 注释清单
# 来源文件: {st_file_path}
# 生成时间: 2026-01-11
# 使用方法: 复制对应的注释内容到GX Works3标签编辑器中

总共 {len(comments)} 个变量注释:

"""
        
        # 按变量类型分组
        inputs = {}
        outputs = {}
        internals = {}
        
        for var_name, comment in comments.items():
            if var_name.lower().startswith('g') and any(x in comment.lower() for x in ['按钮', '开关', '传感器', '反馈']):
                inputs[var_name] = comment
            elif var_name.lower().startswith('g') and any(x in comment.lower() for x in ['接触器', '指示灯', '输出', '阀门']):
                outputs[var_name] = comment
            else:
                internals[var_name] = comment
        
        # 输入变量
        if inputs:
            content += "## 输入变量 (Input Variables)\n"
            content += "```\n"
            for var_name, comment in inputs.items():
                content += f"{var_name:<20} -> {comment}\n"
            content += "```\n\n"
        
        # 输出变量
        if outputs:
            content += "## 输出变量 (Output Variables)\n"
            content += "```\n"
            for var_name, comment in outputs.items():
                content += f"{var_name:<20} -> {comment}\n"
            content += "```\n\n"
        
        # 内部变量
        if internals:
            content += "## 内部变量 (Internal Variables)\n"
            content += "```\n"
            for var_name, comment in internals.items():
                content += f"{var_name:<20} -> {comment}\n"
            content += "```\n\n"
        
        # 添加快速复制格式
        content += "## 快速复制格式 (Quick Copy Format)\n"
        content += "以下格式便于直接复制到GX Works3中:\n\n"
        
        for var_name, comment in comments.items():
            content += f"{comment}\n"
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已生成注释清单: {output_path}")
        return comments

class CommentHelperGUI:
    """图形界面注释助手"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GX Works3 注释助手")
        self.root.geometry("800x600")
        
        self.helper = CommentHelper()
        self.comments = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件选择
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="选择ST文件", command=self.select_st_file).grid(row=0, column=0, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="未选择文件")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        # 注释列表
        list_frame = ttk.LabelFrame(main_frame, text="变量注释列表", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 创建Treeview
        columns = ('变量名', '注释内容')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 定义列
        self.tree.heading('变量名', text='变量名')
        self.tree.heading('注释内容', text='注释内容')
        self.tree.column('变量名', width=200)
        self.tree.column('注释内容', width=400)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=1, sticky=(tk.N, tk.W), padx=(10, 0))
        
        ttk.Button(button_frame, text="复制选中注释", command=self.copy_selected_comment).pack(pady=(0, 5), fill=tk.X)
        ttk.Button(button_frame, text="复制所有注释", command=self.copy_all_comments).pack(pady=(0, 5), fill=tk.X)
        ttk.Button(button_frame, text="生成注释清单", command=self.generate_comment_list).pack(pady=(0, 5), fill=tk.X)
        ttk.Button(button_frame, text="导出JSON", command=self.export_json).pack(pady=(0, 5), fill=tk.X)
        
        # 状态栏
        self.status_label = ttk.Label(main_frame, text="请选择ST文件开始")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
    
    def select_st_file(self):
        """选择ST文件"""
        file_path = filedialog.askopenfilename(
            title="选择ST文件",
            filetypes=[("ST文件", "*.st"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.file_label.config(text=Path(file_path).name)
            self.load_comments(file_path)
    
    def load_comments(self, file_path):
        """加载注释"""
        try:
            self.comments = self.helper.parse_st_comments(file_path)
            
            # 清空现有项目
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 添加新项目
            for var_name, comment in self.comments.items():
                self.tree.insert('', tk.END, values=(var_name, comment))
            
            self.status_label.config(text=f"已加载 {len(self.comments)} 个变量注释")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载文件时出错: {e}")
    
    def copy_selected_comment(self):
        """复制选中的注释"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个变量")
            return
        
        item = self.tree.item(selection[0])
        comment = item['values'][1]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(comment)
        self.status_label.config(text=f"已复制注释: {comment}")
    
    def copy_all_comments(self):
        """复制所有注释"""
        if not self.comments:
            messagebox.showwarning("警告", "没有可复制的注释")
            return
        
        # 生成格式化的注释文本
        comment_text = "\n".join([f"{var}: {comment}" for var, comment in self.comments.items()])
        
        self.root.clipboard_clear()
        self.root.clipboard_append(comment_text)
        self.status_label.config(text=f"已复制 {len(self.comments)} 个注释到剪贴板")
    
    def generate_comment_list(self):
        """生成注释清单文件"""
        if not self.comments:
            messagebox.showwarning("警告", "没有可生成的注释")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="保存注释清单",
            defaultextension=".md",
            filetypes=[("Markdown文件", "*.md"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if output_path:
            try:
                # 使用当前加载的文件路径
                current_file = self.file_label.cget("text")
                self.helper.generate_comment_list(current_file, output_path)
                messagebox.showinfo("成功", f"注释清单已保存到: {output_path}")
            except Exception as e:
                messagebox.showerror("错误", f"生成清单时出错: {e}")
    
    def export_json(self):
        """导出JSON格式"""
        if not self.comments:
            messagebox.showwarning("警告", "没有可导出的注释")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="导出JSON文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(self.comments, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", f"JSON文件已保存到: {output_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出JSON时出错: {e}")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='GX Works3 注释助手工具')
    parser.add_argument('--gui', action='store_true', help='启动图形界面')
    parser.add_argument('--st-file', help='ST源程序文件路径')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.gui:
        # 启动图形界面
        app = CommentHelperGUI()
        app.run()
    else:
        # 命令行模式
        if not args.st_file:
            print("请指定ST文件路径或使用 --gui 启动图形界面")
            return
        
        helper = CommentHelper()
        output_path = args.output or args.st_file.replace('.st', '_comments.md')
        
        print("=== GX Works3 注释助手 ===")
        comments = helper.generate_comment_list(args.st_file, output_path)
        
        if comments:
            print(f"成功处理 {len(comments)} 个变量注释")
            print(f"注释清单已保存到: {output_path}")
        else:
            print("未找到任何注释")

if __name__ == "__main__":
    main()
