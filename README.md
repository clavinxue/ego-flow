# Google Flow (Ego Lite) — `ego-flow`

使用 **Ego Lite (`ego-browser` CLI)** 高效、省 Token 地操作 Google Flow (`https://flow.google.com/`) 的插件。

## 两个宿主版本

| 版本 | 位置 | 适用环境 |
| --- | --- | --- |
| 原版 | 本仓库根目录 | Antigravity + 本地 EGO Lite |
| GPT / Work 版 | [`plugins/ego-flow-gpt/`](plugins/ego-flow-gpt/) | ChatGPT 桌面本地 Work / Codex + 本地 EGO Lite |

GPT 版保留上传、分镜、点数确认和下载能力，增加本地执行检查、标准插件声明与生成超时防重复提交。它是桌面专用插件，不向纯云端对话提供本地浏览器连接。安装、迁移和验证范围见 [GPT 版说明](plugins/ego-flow-gpt/README.md)。

**打包提示**：仓库现在包含两个插件根目录。导入 GPT 插件时请使用发布的 `ego-flow-gpt` 单插件 ZIP，不要导入整个仓库 ZIP。

[下载 GPT 版安装包（v0.1.0）](https://github.com/clavinxue/ego-flow/raw/refs/heads/main/dist/ego-flow-gpt-0.1.0.zip)。如需重新构建，使用 Python 3.9+ 运行 `python3 scripts/package_gpt.py --check` 检查，再运行 `python3 scripts/package_gpt.py` 打包。脚本不覆盖已有 ZIP；迭代后请更新版本或指定新的 `--out`。

## 为什么做这个插件？

借鉴了 `antigravity-flow` 的 Flow 业务经验（防跳转、手动模式、点数校验、0 点数下载避坑），并将底层执行器替换为本地 **Ego Lite 浏览器**：

1. **直接上传本地参考图**：无需复制文件到中转沙盒，也不会在受保护登录页被拦截，支持 `setInputFiles` / `waitForFileChooser` 直接上传绝对路径素材。
2. **更省 Token**：用 `ego-browser nodejs` 单次脚本批量完成导航、参数配置、填词和等待，优先使用 DOM 快照与 `page.evaluate()` 读取状态和点数，仅在最终看图验片时截屏。
3. **直接下载到工作区**：通过 `download.saveAs()` 直接保存到指定项目目录。
4. **无缝人机接管**：遇到登录、人机验证或充值时通过 `task.handOff()` 交给用户在浏览器中完成，随后无缝恢复。

## 包含技能

- `ego-flow-image`：参考图上传与 Nano Banana 图片生成（支持中/英文 UI，0 点数原图下载）。
- `ego-flow-video`：分镜规划、Omni 1.2 Flash / Veo 3.1 视频生成、首尾帧与场景剪辑导出。

> **使用提示**：若同时启用了原版 `antigravity-flow`，其规则会要求走内置 `browser` 子代理。日常使用 Ego Lite 驱动 Flow 时，建议在插件管理中关闭原版 `antigravity-flow`。
