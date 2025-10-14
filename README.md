# 🚀 AI 预制件模板 (Prefab Template)

[![Build and Release](https://github.com/your-org/prefab-template/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/your-org/prefab-template/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/managed%20by-uv-F67909.svg)](https://github.com/astral-sh/uv)
[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-black)](https://flake8.pycqa.org/)

> **这是一个标准化的预制件模板仓库，用于为 AI 编码平台创建可复用的高质量代码模块。**

## 📋 目录

- [什么是预制件？](#什么是预制件)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [开发指南](#开发指南)
- [测试与验证](#测试与验证)
- [发布流程](#发布流程)
- [示例预制件](#示例预制件)
- [常见问题](#常见问题)

**📚 更多文档**: [文档索引](DOCS_INDEX.md) | [架构设计](ARCHITECTURE.md) | [AI助手指南](AGENTS.md)

## 什么是预制件？

预制件 (Prefab) 是一个可被 AI 直接调用的、经过标准化打包的 Python 代码模块。它解决了 AI 在处理复杂业务逻辑时能力不足的问题，通过社区贡献的方式为平台提供高质量、可复用的代码组件。

### 核心特性

- ✅ **标准化结构**: 统一的文件组织和配置规范
- 🤖 **AI 友好**: 明确的函数签名和元数据描述
- 🚀 **自动化 CI/CD**: 一键测试、打包、发布
- 📦 **依赖管理**: 自动打包运行时依赖
- 🔒 **质量保证**: 强制性的代码检查和测试

## 快速开始

### 1. 使用此模板创建新仓库

点击 GitHub 上的 "Use this template" 按钮，或者克隆此仓库：

```bash
git clone https://github.com/your-org/prefab-template.git my-prefab
cd my-prefab
```

### 2. 安装开发依赖

使用现代化的 [uv](https://github.com/astral-sh/uv) 工具：

```bash
# 安装 uv（如果尚未安装）
# Windows: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖（自动创建虚拟环境）
uv sync --dev
```

### 3. 编写你的预制件

1. **编辑 `src/main.py`**: 在这里编写你的核心业务逻辑
2. **更新 `prefab-manifest.json`**: 描述你的函数签名和元数据
3. **编写测试**: 在 `tests/test_main.py` 中添加单元测试

### 4. 本地测试

```bash
# 运行测试
uv run pytest tests/ -v

# 代码风格检查
uv run flake8 src/ --max-line-length=120

# 验证 manifest 一致性
uv run python scripts/validate_manifest.py

# 一键运行所有验证
uv run python scripts/quick_start.py
```

### 5. 发布预制件

```bash
# 方式一: 使用版本升级脚本（推荐）
uv run python scripts/version_bump.py patch  # 1.0.0 -> 1.0.1
# 或
uv run python scripts/version_bump.py minor  # 1.0.0 -> 1.1.0
# 或
uv run python scripts/version_bump.py major  # 1.0.0 -> 2.0.0

# 然后提交并推送
git add .
git commit -m "Bump version to x.x.x"
git tag vx.x.x
git push origin vx.x.x

# 方式二: 手动更新
# 1. 手动编辑 prefab-manifest.json 和 pyproject.toml 中的 version
# 2. git tag v1.0.0
# 3. git push origin v1.0.0
```

🎉 GitHub Actions 将自动完成测试、打包和发布！

## 项目结构

```
prefab-template/
├── .github/
│   └── workflows/
│       └── build-and-release.yml    # CI/CD 自动化流程
├── src/
│   └── main.py                      # 预制件核心代码（必须）
├── tests/
│   └── test_main.py                 # 单元测试
├── scripts/
│   └── validate_manifest.py         # Manifest 验证脚本
├── prefab-manifest.json             # 预制件元数据（必须）
├── pyproject.toml                   # 项目配置和依赖
├── .gitignore                       # Git 忽略文件
├── LICENSE                          # 开源许可证
└── README.md                        # 项目文档
```

## 开发指南

### `src/main.py` - 核心业务逻辑

这是你的预制件的唯一入口文件。所有暴露给 AI 的函数都必须在此文件中定义。

**示例函数：**

```python
def analyze_dataset(data: list, operation: str = "statistics") -> dict:
    """
    分析数据集并返回统计结果
    
    Args:
        data: 数字列表
        operation: 操作类型 ("statistics", "sum", "average")
    
    Returns:
        包含分析结果的字典
    """
    try:
        if not data:
            return {
                "success": False,
                "error": "数据集不能为空",
                "error_code": "EMPTY_DATA"
            }
        
        if operation == "statistics":
            stats = calculate_statistics(data)
            return {
                "success": True,
                "data": {
                    "operation": "statistics",
                    "statistics": stats
                }
            }
        # ... 其他操作类型
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }
```

**编码规范：**

- ✅ 使用类型提示 (Type Hints)
- ✅ 编写清晰的 Docstring
- ✅ 返回结构化的数据（通常是字典）
- ✅ 包含错误处理
- ❌ 避免使用全局状态
- ❌ 不要在模块级别执行副作用操作

### `prefab-manifest.json` - 元数据描述

这是 AI 理解如何调用你的预制件的"API 契约"。**必须**与 `src/main.py` 中的函数签名保持一致。

**字段说明：**

```json
{
  "schema_version": "1.0",           // 清单模式版本（固定）
  "id": "hello-world-prefab",        // 全局唯一的预制件 ID
  "version": "1.0.0",                // 语义化版本号（与 Git Tag 一致）
  "entry_point": "src/main.py",      // 入口文件（固定）
  "dependencies_file": "pyproject.toml",  // 依赖文件（固定）
  "functions": [                     // 函数列表
    {
      "name": "analyze_dataset",     // 函数名（必须与代码一致）
      "description": "分析数据集并返回统计结果",  // 功能描述
      "parameters": [                // 参数列表
        {
          "name": "data",
          "type": "list",
          "description": "数字列表",
          "required": true
        },
        {
          "name": "operation",
          "type": "str",
          "description": "操作类型：'statistics', 'sum', 'average'",
          "required": false,
          "default": "statistics"
        }
      ],
      "returns": {                   // 返回值描述（结构化 schema）
        "type": "object",
        "description": "返回结果对象",
        "properties": {
          "success": {
            "type": "boolean",
            "description": "操作是否成功"
          },
          "data": {
            "type": "object",
            "description": "成功时的结果数据",
            "optional": true
          },
          "error": {
            "type": "string",
            "description": "错误信息",
            "optional": true
          },
          "error_code": {
            "type": "string",
            "description": "错误代码",
            "optional": true
          }
        }
      }
    }
  ]
}
```

### 依赖管理

在 `pyproject.toml` 中添加你的依赖：

```toml
[project]
# 运行时依赖（会被打包到最终产物中）
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[project.optional-dependencies]
# 开发/测试依赖（不会被打包）
dev = [
    "pytest>=7.4.0",
    "flake8>=6.1.0",
    "pytest-cov>=4.1.0",
]
```

**使用 uv 管理依赖：**

```bash
# 添加运行时依赖
uv add requests pandas

# 添加开发依赖
uv add --dev pytest flake8

# 同步依赖
uv sync --dev
```

## 测试与验证

### 单元测试

使用 Pytest 编写测试：

```python
# tests/test_main.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import analyze_dataset

def test_analyze_dataset():
    result = analyze_dataset([1, 2, 3, 4, 5], "statistics")
    assert result["success"] is True
    assert result["data"]["statistics"]["average"] == 3.0
```

运行测试：

```bash
pytest tests/ -v
```

### Manifest 验证

验证 `prefab-manifest.json` 与代码的一致性：

```bash
python scripts/validate_manifest.py
```

此脚本会检查：
- ✅ Manifest 中声明的函数是否都存在于 `main.py`
- ✅ 函数参数的名称和必选/可选属性是否匹配
- ⚠️  `main.py` 中的公共函数是否都在 Manifest 中声明

## 发布流程

### 自动化发布（推荐）

整个发布流程完全自动化，你只需要：

1. **更新版本号**: 编辑 `prefab-manifest.json`，修改 `version` 字段
2. **提交更改**: `git add . && git commit -m "Release v1.0.0"`
3. **创建标签**: `git tag v1.0.0`（版本号必须与 manifest 一致）
4. **推送标签**: `git push origin v1.0.0`

GitHub Actions 将自动执行以下步骤：

```mermaid
graph LR
    A[推送 Tag] --> B[代码检查]
    B --> C[运行测试]
    C --> D[验证 Manifest]
    D --> E[打包预制件]
    E --> F[创建 Release]
    F --> G[上传附件]
```

### 发布产物

- **格式**: `{id}-{version}.tar.gz`（例如 `hello-world-prefab-1.0.0.tar.gz`）
- **内容**: `src/` 目录 + `prefab-manifest.json` + `vendor/`（依赖）
- **位置**: GitHub Release 附件

## 示例预制件

本模板自带一个完整的科学计算示例预制件，包含一个功能丰富的函数：

### `analyze_dataset(data, operation)` - 数据集分析

支持多种操作类型：

```python
# 完整统计
result = analyze_dataset([1, 2, 3, 4, 5], "statistics")
# {"success": True, "data": {"operation": "statistics", "statistics": {...}}}

# 求和
result = analyze_dataset([10, 20, 30], "sum")
# {"success": True, "data": {"operation": "sum", "value": 60, "count": 3}}

# 平均值
result = analyze_dataset([2, 4, 6], "average")
# {"success": True, "data": {"operation": "average", "value": 4.0, "count": 3}}
```

你可以直接修改这个示例，或者完全替换为自己的业务逻辑。

## AI 集成说明

当你的预制件发布后，AI 平台将能够：

1. **自动发现**: 通过 `prefab-manifest.json` 理解预制件的功能
2. **智能调用**: 根据用户的自然语言需求，选择合适的函数并传递参数
3. **解释结果**: 将函数返回值转换为用户友好的输出

**用户体验示例：**

> 用户: "帮我分析这组数据的统计信息：[10, 20, 30, 40, 50]"  
> AI: *调用 `analyze_dataset([10, 20, 30, 40, 50], "statistics")`*  
> AI: "已完成分析：共 5 个数据点，平均值 30.0，最大值 50，最小值 10"

## 常见问题

### Q: 我可以使用第三方库吗？

**A**: 当然可以！使用 `uv add package-name` 添加运行时依赖，CI/CD 会自动打包。

```bash
# 添加运行时依赖（会被打包）
uv add requests pandas

# 添加开发依赖（不会被打包）
uv add --dev pytest-mock
```

### Q: 如何处理敏感信息（如 API Key）？

**A**: 
1. 通过函数参数传递（推荐）
2. 使用环境变量，并在 README 中说明配置要求
3. **绝对不要**将密钥硬编码到代码中

### Q: 可以添加多个 `.py` 文件吗？

**A**: 可以！你可以在 `src/` 目录中创建多个模块，但 `main.py` 必须是唯一的入口点。

**示例结构：**
```
src/
├── main.py                    # 主入口文件
├── utils/                     # 工具模块包
│   ├── __init__.py
│   └── math_utils.py         # 数学工具
└── other_module.py           # 其他模块（可选）
```

**使用方式：**
```python
# src/main.py
try:
    # 优先使用相对导入（打包时）
    from .utils import helper_function
except ImportError:
    # 回退到绝对导入（开发/测试时）
    from utils import helper_function

def my_function():
    return helper_function()
```

本模板已包含完整的多文件示例，参见 `src/utils/` 目录和 `analyze_numbers` 函数。

### Q: 如何调试 CI/CD 失败？

**A**: 
1. 查看 GitHub Actions 的日志输出
2. 本地运行相同的命令进行复现：
   - `pytest tests/` - 测试失败？
   - `flake8 src/` - 代码风格问题？
   - `python scripts/validate_manifest.py` - Manifest 不一致？

### Q: 版本号规范是什么？

**A**: 遵循语义化版本 (Semantic Versioning):
- **主版本号 (MAJOR)**: 不兼容的 API 更改
- **次版本号 (MINOR)**: 向后兼容的功能新增
- **修订号 (PATCH)**: 向后兼容的问题修复

示例: `v1.2.3` → `1.2.3`

### Q: 可以发布私有预制件吗？

**A**: 可以！将仓库设为私有即可。Release 也会是私有的。

## 贡献指南

欢迎为此模板贡献改进！请：

1. Fork 此仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 支持与反馈

- 📖 [文档](https://github.com/your-org/prefab-template/wiki)
- 🐛 [问题反馈](https://github.com/your-org/prefab-template/issues)
- 💬 [讨论区](https://github.com/your-org/prefab-template/discussions)

---

**祝你开发愉快！🎉**

_如果这个模板对你有帮助，请给我们一个 ⭐ Star！_

