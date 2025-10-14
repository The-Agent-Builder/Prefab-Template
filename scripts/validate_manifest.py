#!/usr/bin/env python3
"""
验证 prefab-manifest.json 与 src/main.py 的一致性

此脚本检查：
1. manifest.json 中声明的所有函数在 main.py 中都存在
2. 函数参数的数量和名称匹配
3. manifest.json 的格式正确
"""

import json
import sys
import os
import ast
import inspect
from pathlib import Path


def load_manifest():
    """加载并解析 manifest 文件"""
    manifest_path = Path("prefab-manifest.json")
    if not manifest_path.exists():
        print("❌ 错误: prefab-manifest.json 文件不存在")
        return None
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        return manifest
    except json.JSONDecodeError as e:
        print(f"❌ 错误: prefab-manifest.json 格式不正确: {e}")
        return None


def extract_function_signatures(main_py_path):
    """从 main.py 提取函数签名"""
    if not main_py_path.exists():
        print(f"❌ 错误: {main_py_path} 文件不存在")
        return None
    
    try:
        with open(main_py_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        print(f"❌ 错误: {main_py_path} 语法错误: {e}")
        return None
    
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 只提取模块级别的函数（不在类内部）
            if isinstance(node.parent if hasattr(node, 'parent') else None, ast.Module) or \
               not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) 
                      if hasattr(parent, 'body') and node in getattr(parent, 'body', [])):
                params = []
                defaults_start = len(node.args.args) - len(node.args.defaults)
                
                for i, arg in enumerate(node.args.args):
                    param_info = {
                        'name': arg.arg,
                        'required': i < defaults_start
                    }
                    params.append(param_info)
                
                functions[node.name] = params
    
    return functions


def validate_manifest_schema(manifest):
    """验证 manifest 的基本模式"""
    required_fields = ['schema_version', 'id', 'version', 'entry_point', 'dependencies_file', 'functions']
    
    for field in required_fields:
        if field not in manifest:
            print(f"❌ 错误: manifest 缺少必需字段: {field}")
            return False
    
    if manifest['entry_point'] != 'src/main.py':
        print(f"❌ 错误: entry_point 必须是 'src/main.py', 当前值: {manifest['entry_point']}")
        return False
    
    if manifest['dependencies_file'] != 'pyproject.toml':
        print(f"❌ 错误: dependencies_file 必须是 'pyproject.toml', 当前值: {manifest['dependencies_file']}")
        return False
    
    return True


def validate_functions(manifest, actual_functions):
    """验证函数定义的一致性"""
    errors = []
    warnings = []
    
    manifest_functions = {f['name']: f for f in manifest['functions']}
    
    # 检查 manifest 中的函数是否都在 main.py 中存在
    for func_name, func_def in manifest_functions.items():
        if func_name not in actual_functions:
            errors.append(f"函数 '{func_name}' 在 manifest 中声明但在 main.py 中不存在")
            continue
        
        # 验证参数
        manifest_params = {p['name']: p for p in func_def.get('parameters', [])}
        actual_params = {p['name']: p for p in actual_functions[func_name]}
        
        # 检查必需参数
        for param_name, param_info in manifest_params.items():
            if param_name not in actual_params:
                errors.append(f"函数 '{func_name}': 参数 '{param_name}' 在 manifest 中声明但在实际函数中不存在")
            elif param_info.get('required', False) and not actual_params[param_name]['required']:
                warnings.append(f"函数 '{func_name}': 参数 '{param_name}' 在 manifest 中标记为必需，但在函数中有默认值")
        
        # 检查实际参数是否都在 manifest 中
        for param_name, param_info in actual_params.items():
            if param_name not in manifest_params:
                warnings.append(f"函数 '{func_name}': 参数 '{param_name}' 在函数中存在但未在 manifest 中声明")
        
        # 验证返回值定义
        if 'returns' not in func_def:
            errors.append(f"函数 '{func_name}': 缺少 'returns' 字段定义")
        else:
            returns = func_def['returns']
            
            # 检查必需的字段
            if 'type' not in returns:
                errors.append(f"函数 '{func_name}': returns 缺少 'type' 字段")
            
            if 'description' not in returns:
                warnings.append(f"函数 '{func_name}': returns 缺少 'description' 字段")
            
            # 如果是 object 类型，建议定义 properties
            if returns.get('type') == 'object':
                if 'properties' not in returns:
                    warnings.append(f"函数 '{func_name}': returns 是 object 类型，建议定义 'properties' 以详细描述结构")
                else:
                    # 检查 properties 中的每个字段是否有 type 和 description
                    for prop_name, prop_def in returns['properties'].items():
                        if 'type' not in prop_def:
                            warnings.append(f"函数 '{func_name}': returns.properties.{prop_name} 缺少 'type' 字段")
                        if 'description' not in prop_def:
                            warnings.append(f"函数 '{func_name}': returns.properties.{prop_name} 缺少 'description' 字段")
    
    # 检查 main.py 中是否有未声明的公共函数
    for func_name in actual_functions:
        if not func_name.startswith('_') and func_name not in manifest_functions:
            warnings.append(f"函数 '{func_name}' 在 main.py 中定义但未在 manifest 中声明")
    
    return errors, warnings


def main():
    """主验证流程"""
    print("🔍 开始验证 prefab-manifest.json 与 src/main.py 的一致性...\n")
    
    # 加载 manifest
    manifest = load_manifest()
    if not manifest:
        sys.exit(1)
    
    # 验证 manifest 模式
    if not validate_manifest_schema(manifest):
        sys.exit(1)
    
    print("✅ Manifest 基本模式验证通过")
    
    # 提取实际函数签名
    main_py_path = Path("src/main.py")
    actual_functions = extract_function_signatures(main_py_path)
    if actual_functions is None:
        sys.exit(1)
    
    print(f"✅ 成功解析 main.py，发现 {len(actual_functions)} 个函数")
    
    # 验证函数一致性
    errors, warnings = validate_functions(manifest, actual_functions)
    
    # 输出结果
    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print("\n❌ 错误:")
        for error in errors:
            print(f"  - {error}")
        print("\n验证失败! 请修复上述错误。")
        sys.exit(1)
    
    print("\n✅ 验证成功! Manifest 与 main.py 完全一致。")
    sys.exit(0)


if __name__ == "__main__":
    main()

