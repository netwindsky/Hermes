# 贡献指南

感谢您对 Hermes 项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 添加新功能

## 开始之前

在开始贡献之前，请确保您已经：

1. 阅读了项目的 [README.md](README.md)
2. 了解了项目的基本架构和功能
3. 查看了现有的 [Issues](https://github.com/netwindsky/Hermes/issues) 和 [Pull Requests](https://github.com/netwindsky/Hermes/pulls)

## 如何贡献

### 报告 Bug

如果您发现了 Bug，请：

1. 在 [Issues](https://github.com/netwindsky/Hermes/issues) 中搜索是否已有相关报告
2. 如果没有，请创建新的 Issue，包含：
   - 清晰的标题和描述
   - 重现步骤
   - 预期行为和实际行为
   - 环境信息（Python版本、操作系统等）
   - 相关的错误日志或截图

### 提出功能建议

如果您有新功能的想法：

1. 在 Issues 中搜索是否已有类似建议
2. 创建新的 Feature Request，包含：
   - 功能的详细描述
   - 使用场景和价值
   - 可能的实现方案

### 提交代码

#### 开发环境设置

1. Fork 项目到您的 GitHub 账户
2. 克隆您的 Fork：
   ```bash
   git clone https://github.com/YOUR_USERNAME/Hermes.git
   cd Hermes
   ```

3. 创建虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 或
   .venv\Scripts\activate     # Windows
   ```

4. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

#### 开发流程

1. 创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. 进行开发并测试
3. 提交更改：
   ```bash
   git add .
   git commit -m "feat: add new feature" # 使用语义化提交信息
   ```

4. 推送到您的 Fork：
   ```bash
   git push origin feature/your-feature-name
   ```

5. 创建 Pull Request

#### 代码规范

- 遵循 PEP 8 Python 代码风格
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 保持代码简洁和可读性

#### 提交信息规范

使用语义化提交信息：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: add support for custom headers in crawler
fix: resolve memory leak in task scheduler
docs: update installation guide
```

### Pull Request 指南

创建 Pull Request 时，请确保：

1. **标题清晰**：简洁描述更改内容
2. **描述详细**：说明更改的原因和影响
3. **关联 Issue**：如果相关，请引用对应的 Issue
4. **测试充分**：确保新代码经过测试
5. **文档更新**：如需要，更新相关文档

### Pull Request 模板

```markdown
## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 其他

## 更改描述
简要描述此次更改的内容和原因。

## 相关 Issue
关闭 #(issue编号)

## 测试
描述您如何测试了这些更改。

## 检查清单
- [ ] 代码遵循项目的代码规范
- [ ] 进行了自我代码审查
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 测试通过
```

## 开发指南

### 项目结构

```
Hermes/
├── core/                    # 核心功能模块
│   ├── config/             # 配置管理
│   ├── crawl/              # 爬虫核心
│   ├── storage/            # 数据存储
│   ├── task/               # 任务调度
│   └── web/                # Web API
├── config/                 # 配置文件
├── data/                   # 数据存储目录
├── docs/                   # 项目文档
└── tests/                  # 测试文件
```

### 添加新功能

1. 在相应的模块中添加功能
2. 更新配置文件（如需要）
3. 添加测试用例
4. 更新文档

### 调试技巧

- 使用项目的日志系统进行调试
- 查看 `system.log` 文件获取运行时信息
- 使用 Python 调试器进行断点调试

## 社区准则

- 保持友善和专业的态度
- 尊重不同的观点和经验水平
- 提供建设性的反馈
- 帮助新贡献者融入社区

## 获得帮助

如果您在贡献过程中遇到问题：

1. 查看项目文档
2. 在 Issues 中搜索相关问题
3. 创建新的 Issue 寻求帮助

## 许可证

通过贡献代码，您同意您的贡献将在 [MIT License](LICENSE) 下发布。

---

再次感谢您的贡献！🎉