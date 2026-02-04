# 鸣潮插件单元测试说明

## 测试概览

本插件包含完整的单元测试套件，涵盖所有核心模块：

| 测试文件 | 测试内容 | 测试数量 |
|---------|---------|---------|
| `conftest.py` | pytest fixtures 和测试数据 | - |
| `test_utils.py` | 工具函数测试 | 15+ |
| `test_models.py` | 数据模型测试 | 20+ |
| `test_statistics.py` | 统计模块测试 | 15+ |
| `test_waves_api.py` | API模块测试 | 15+ |
| `test_integration.py` | 集成测试 | 10+ |

## 环境准备

### 安装测试依赖

```bash
pip install pytest pytest-asyncio pytest-mock httpx
```

### 或使用 pyproject.toml

确保 `pyproject.toml` 中包含测试依赖：

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.10.0",
    "httpx>=0.24.0",
]
```

安装测试依赖：

```bash
pip install -e ".[test]"
```

## 运行测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试文件

```bash
# 测试工具函数
pytest tests/test_utils.py -v

# 测试数据模型
pytest tests/test_models.py -v

# 测试统计模块
pytest tests/test_statistics.py -v

# 测试API模块
pytest tests/test_waves_api.py -v

# 测试集成功能
pytest tests/test_integration.py -v
```

### 运行特定测试类或方法

```bash
# 运行特定测试类
pytest tests/test_utils.py::TestRoleNameMapping -v

# 运行特定测试方法
pytest tests/test_utils.py::TestRoleNameMapping::test_get_role_id_by_name_success -v
```

### 显示详细输出

```bash
pytest tests/ -v -s
```

### 显示覆盖率报告

```bash
pytest tests/ --cov=nonebot_plugin_wwuid --cov-report=html
```

### 运行快速测试（跳过慢速测试）

```bash
pytest tests/ -v -m "not slow"
```

## 测试结构

### conftest.py - 测试配置

提供以下 fixtures：

- `test_user_id`: 测试用户ID
- `test_game_uid`: 测试游戏UID
- `test_ck`: 测试CK
- `test_role_id`: 测试角色ID
- `test_role_name`: 测试角色名
- `mock_role_data`: 模拟角色数据
- `mock_role_detail_data`: 模拟角色详情数据
- `temp_cache_dir`: 临时缓存目录
- `mock_api_response_success`: 模拟成功的API响应
- `mock_api_response_error`: 模拟失败的API响应
- `event_loop`: 事件循环

### test_utils.py - 工具函数测试

测试内容：

- ✅ 角色名称映射（ID <-> 名称）
- ✅ 角色名标准化
- ✅ 数字安全转换（int/float）
- ✅ 数字格式化
- ✅ 文本截断
- ✅ 缓存读写
- ✅ 缓存过期检查
- ✅ 角色信息格式化

### test_models.py - 数据模型测试

测试内容：

- ✅ 所有 Pydantic 模型验证
- ✅ 命座数据模型
- ✅ 武器数据模型
- ✅ 声骸数据模型
- ✅ 技能数据模型
- ✅ 角色数据模型
- ✅ 角色详情数据模型
- ✅ 账户基础信息模型
- ✅ 角色列表模型
- ✅ 模型方法（get_chain_num, get_skill_level 等）

### test_statistics.py - 统计模块测试

测试内容：

- ✅ 统计管理器初始化
- ✅ 默认权重配置
- ✅ 等级评分计算
- ✅ 命座评分计算
- ✅ 武器评分计算
- ✅ 声骸评分计算
- ✅ 技能评分计算
- ✅ 单角色评分计算
- ✅ 详细评分数据

### test_waves_api.py - API模块测试

测试内容：

- ✅ WavesApiResponse 响应类
- ✅ WavesApi 类初始化
- ✅ 服务器ID获取
- ✅ 请求头构建
- ✅ GET/POST 请求
- ✅ 超时处理
- ✅ 网络错误处理
- ✅ 登录校验
- ✅ 获取基础信息
- ✅ 获取角色列表
- ✅ 获取角色详情
- ✅ 刷新数据
- ✅ JWT Token 生成

### test_integration.py - 集成测试

测试内容：

- ✅ 缓存完整生命周期
- ✅ 角色名称双向映射
- ✅ 多角色映射
- ✅ 多角色评分计算
- ✅ 统计权重总和验证
- ✅ 角色评分排序
- ✅ 完整数据处理流程
- ✅ 错误处理集成
- ✅ 性能测试
- ✅ 真实用户场景模拟

## 本地测试脚本

### 快速运行所有测试

创建 `run_tests.bat` (Windows):

```batch
@echo off
echo Running tests...
pytest tests/ -v --tb=short
pause
```

创建 `run_tests.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "Running tests..."
pytest tests/ -v --tb=short
```

### 运行并生成覆盖率报告

```bash
pytest tests/ --cov=nonebot_plugin_wwuid --cov-report=term-missing --cov-report=html
```

## 持续集成

### GitHub Actions 配置示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
      - name: Run tests
        run: |
          pytest tests/ -v --cov=nonebot_plugin_wwuid --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 常见问题

### Q: 测试失败，提示模块未找到？

A: 确保在项目根目录运行测试，并且已经安装了插件：

```bash
pip install -e .
```

### Q: 异步测试失败？

A: 确保安装了 pytest-asyncio：

```bash
pip install pytest-asyncio
```

### Q: 如何跳过需要真实API的测试？

A: 使用 pytest 的标记功能，或者确保所有API测试都使用了 mock。

### Q: 如何调试测试？

A: 使用 `-s` 参数显示输出，或使用 `pdb.settrace()` 在代码中设置断点：

```bash
pytest tests/test_utils.py::TestRoleNameMapping::test_get_role_id_by_name_success -v -s
```

## 添加新测试

### 1. 在对应测试文件中添加测试方法

```python
def test_new_feature(self):
    """测试新功能"""
    result = some_function()
    assert result == expected_value
```

### 2. 运行新测试

```bash
pytest tests/test_xxx.py::TestClassName::test_new_feature -v
```

### 3. 确保测试通过

```bash
pytest tests/ -v
```

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|------|-----------|
| utils.py | 90%+ |
| models.py | 85%+ |
| statistics.py | 90%+ |
| waves_api.py | 80%+ |
| refresh.py | 75%+ |
| query.py | 75%+ |
| overall | 80%+ |

## 最佳实践

1. ✅ 每个测试只测试一个功能点
2. ✅ 使用描述性的测试名称
3. ✅ 使用 fixtures 复用测试数据
4. ✅ 对异步测试使用 `@pytest.mark.asyncio`
5. ✅ 使用 mock 隔离外部依赖
6. ✅ 确保测试独立，不依赖执行顺序
7. ✅ 定期运行测试，保持代码质量
8. ✅ 为新功能添加对应的测试

## 更新日志

### v1.0.0
- 初始测试套件
- 覆盖所有核心模块
- 包含单元测试和集成测试
- 支持本地测试和CI/CD
