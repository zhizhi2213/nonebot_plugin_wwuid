# 测试用例快速参考

## 测试文件清单

| 文件 | 测试类数量 | 测试方法数量 | 说明 |
|------|-----------|------------|------|
| conftest.py | - | - | 测试配置和fixtures |
| test_utils.py | 5 | 15+ | 工具函数测试 |
| test_models.py | 9 | 20+ | 数据模型测试 |
| test_statistics.py | 2 | 15+ | 统计模块测试 |
| test_waves_api.py | 3 | 15+ | API模块测试 |
| test_integration.py | 6 | 10+ | 集成测试 |

## test_utils.py - 测试用例

### TestRoleNameMapping (角色名称映射测试)

```python
test_get_role_id_by_name_success()      # 通过角色名获取ID - 成功
test_get_role_id_by_name_not_found()   # 通过角色名获取ID - 未找到
test_get_role_name_by_id_success()      # 通过ID获取角色名 - 成功
test_get_role_name_by_id_not_found()     # 通过ID获取角色名 - 未找到
test_normalize_role_name()              # 角色名标准化
```

### TestNumberUtils (数字工具函数测试)

```python
test_safe_int_success()      # 安全转整数 - 成功
test_safe_int_default()      # 安全转整数 - 使用默认值
test_safe_float_success()    # 安全转浮点数 - 成功
test_safe_float_default()    # 安全转浮点数 - 使用默认值
test_format_number_int()     # 格式化数字 - 整数
test_format_number_float()   # 格式化数字 - 浮点数
```

### TestTextUtils (文本工具函数测试)

```python
test_truncate_text_no_truncate()  # 截断文本 - 不需要截断
test_truncate_text_truncate()      # 截断文本 - 需要截断
```

### TestCacheUtils (缓存工具函数测试)

```python
test_save_and_load_user_cache()      # 保存和加载用户缓存
test_load_user_cache_not_found()     # 加载用户缓存 - 文件不存在
test_save_and_load_role_cache()       # 保存和加载角色缓存
test_is_cache_expired_true()          # 缓存过期检查 - 已过期
test_is_cache_expired_false()         # 缓存过期检查 - 未过期
test_is_cache_expired_exact()         # 缓存过期检查 - 刚好过期
```

### TestFormatRoleInfo (角色信息格式化测试)

```python
test_format_role_info_with_mock_role()  # 格式化角色信息
```

## test_models.py - 测试用例

### TestChain (命座模型测试)

```python
test_chain_valid_data()     # 创建有效的命座数据
test_chain_minimal_data()   # 创建最小命座数据
```

### TestWeapon (武器模型测试)

```python
test_weapon_valid_data()  # 创建有效的武器数据
```

### TestWeaponData (武器数据模型测试)

```python
test_weapon_data_valid()  # 创建有效的武器数据
```

### TestPhantom (声骸模型测试)

```python
test_phantom_prop_valid()   # 创建有效的声骸属性
test_fetter_detail_valid()  # 创建有效的声骸共鸣
test_props_valid()          # 创建有效的属性词条
test_equip_phantom_valid()   # 创建有效的装备声骸
```

### TestSkill (技能模型测试)

```python
test_skill_valid()    # 创建有效的技能
test_skill_data_valid()  # 创建有效的技能数据
```

### TestRole (角色模型测试)

```python
test_role_valid()  # 创建有效的角色
```

### TestRoleDetailData (角色详情数据模型测试)

```python
test_role_detail_data_valid()        # 创建有效的角色详情数据
test_get_chain_num()                # 获取命座数量
test_get_chain_name()               # 获取命座名称
test_get_chain_name_six_chains()    # 六链命座名称
test_get_skill_level()              # 获取指定技能等级
test_get_skill_list()              # 获取排序后的技能列表
test_get_skill_branch_no_active()    # 获取技能分支 - 无激活分支
test_get_phantom_count()            # 获取声骸数量
```

### TestAccountBaseInfo (账户基础信息模型测试)

```python
test_account_base_info_valid()  # 创建有效的账户基础信息
test_account_base_info_partial()  # 部分账户信息
```

### TestRoleList (角色列表模型测试)

```python
test_role_list_valid()  # 创建有效的角色列表
```

## test_statistics.py - 测试用例

### TestStatisticsManager (统计管理器测试)

```python
test_init_statistics_manager()         # 初始化统计管理器
test_get_default_weight_config()       # 获取默认权重配置
test_calculate_level_score_max()       # 等级评分 - 满分
test_calculate_level_score_mid()       # 等级评分 - 中等
test_calculate_level_score_low()       # 等级评分 - 低分
test_calculate_chain_score_max()       # 命座评分 - 满分
test_calculate_chain_score_half()      # 命座评分 - 半数
test_calculate_chain_score_zero()      # 命座评分 - 零命
test_calculate_chain_score_4star()    # 命座评分 - 4星角色
test_calculate_weapon_score_max()      # 武器评分 - 满分
test_calculate_weapon_score_mid()      # 武器评分 - 中等
test_calculate_phantom_score_full()    # 声骸评分 - 全装备高品质
test_calculate_phantom_score_partial() # 声骸评分 - 部分装备
test_calculate_phantom_score_zero()    # 声骸评分 - 无装备
test_calculate_skill_score_max()       # 技能评分 - 满级
test_calculate_skill_score_mid()       # 技能评分 - 中等
test_calculate_single_role_score()      # 计算单个角色评分
test_calculate_single_role_score_detail_scores()  # 计算单个角色评分 - 详细评分
```

### TestRoleScore (角色评分数据类测试)

```python
test_role_score_creation()     # 创建角色评分
test_role_score_default_values()  # 角色评分默认值
```

## test_waves_api.py - 测试用例

### TestWavesApiResponse (API响应类测试)

```python
test_response_success()      # 成功的响应
test_response_failure()      # 失败的响应
test_throw_msg()            # 获取错误消息
test_throw_msg_default()    # 获取默认错误消息
test_model_dump()          # 序列化为字典
```

### TestWavesApi (WavesApi类测试)

```python
test_init()                         # 初始化
test_close()                        # 关闭客户端
test_get_server_id_default()         # 获取服务器ID - 默认
test_get_server_id_foreign()         # 获取服务器ID - 外服
test_get_server_id_invalid()         # 获取服务器ID - 无效ID
test_get_headers()                  # 获取请求头
test_request_get_success()          # GET请求 - 成功
test_request_post_success()         # POST请求 - 成功
test_request_timeout()              # 请求超时
test_request_network_error()        # 网络错误
test_login_log()                   # 登录校验
test_get_base_info()               # 获取账户基础信息
test_get_role_info()               # 获取角色列表
test_get_role_detail_info()         # 获取单个角色详情
test_refresh_data()                # 刷新数据
test_get_owned_role_info()          # 获取已拥有角色信息
```

### TestGenerateRandomJwtToken (生成随机JWT Token测试)

```python
test_generate_token_length()   # 生成Token长度
test_generate_token_format()   # 生成Token格式
test_generate_token_unique()   # 生成Token唯一性
```

## test_integration.py - 测试用例

### TestIntegrationCache (缓存集成测试)

```python
test_cache_lifecycle()  # 缓存完整生命周期
```

### TestIntegrationRoleMapping (角色映射集成测试)

```python
test_role_name_bidirectional_mapping()  # 角色名称双向映射
test_multiple_roles_mapping()          # 多个角色映射
```

### TestIntegrationStatistics (统计集成测试)

```python
test_calculate_multiple_roles()   # 计算多个角色评分
test_statistics_weight_sum()      # 统计权重总和
test_role_score_ordering()        # 角色评分排序
```

### TestIntegrationDataFlow (数据流集成测试)

```python
test_full_data_processing_flow()  # 完整数据处理流程
```

### TestIntegrationErrorHandling (错误处理集成测试)

```python
test_handle_invalid_role_data()   # 处理无效角色数据
test_handle_missing_role_name()   # 处理缺失角色名
test_handle_cache_not_found()     # 处理缓存未找到
```

### TestIntegrationPerformance (性能集成测试)

```python
test_bulk_role_mapping_lookup()    # 批量角色映射查找性能
test_bulk_score_calculation()     # 批量评分计算性能
```

### TestRealScenario (真实场景测试)

```python
test_user_journey_scenario()  # 模拟用户使用场景
```

## 快速测试命令

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定文件
pytest tests/test_utils.py -v

# 运行特定类
pytest tests/test_utils.py::TestRoleNameMapping -v

# 运行特定方法
pytest tests/test_utils.py::TestRoleNameMapping::test_get_role_id_by_name_success -v

# 运行并显示输出
pytest tests/ -v -s

# 运行并生成覆盖率报告
pytest tests/ --cov=nonebot_plugin_wwuid --cov-report=html

# 只运行单元测试
pytest tests/ -v -m unit

# 只运行集成测试
pytest tests/ -v -m integration

# 跳过慢速测试
pytest tests/ -v -m "not slow"
```

## 测试覆盖率目标

| 模块 | 目标 | 当前 |
|------|------|------|
| utils.py | 90%+ | - |
| models.py | 85%+ | - |
| statistics.py | 90%+ | - |
| waves_api.py | 80%+ | - |
| refresh.py | 75%+ | - |
| query.py | 75%+ | - |
| commands.py | 70%+ | - |
| config.py | 70%+ | - |
| errors.py | 80%+ | - |
| **Total** | **80%+** | **-** |

运行 `pytest tests/ --cov=nonebot_plugin_wwuid --cov-report=term-missing` 查看实际覆盖率。
