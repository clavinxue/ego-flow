# Google Flow (Ego Lite) Operating Rules

These rules apply whenever the user works with **Google Flow** (`https://flow.google.com`) using the `ego-flow` plugin.

## 1. Execution Engine: Ego Lite (`ego-browser` CLI)

- Drive Google Flow through **`ego-browser nodejs`** scripts (running in your local Ego Lite Chromium browser) instead of Antigravity's built-in `browser` subagent.
- Before the first browser action in a session, read `ego-browser skill` (only if not yet loaded in context) and follow its TaskSpace lifecycle (`taskSpace`, `adopt`, `handOff`, `finish({ keep })`).
- **Sandbox rule**: `ego-browser` talks to the local Ego Lite runtime outside the workspace sandbox, so run `ego-browser` commands directly with `BypassSandbox: true` (do not chain unrelated workspace file ops in the same unsandboxed command).
- **Keep the Flow tab alive when iterating**: At the end of a reply, if the user is likely to continue iterating on the same Flow project (e.g., checkpoint pause before generation, or reviewing generated candidates), finish with `await task.finish({ keep: [page.label] })` so the next turn can `claimTaskSpace(SPACE_ID)` without reloading. Use `keep: []` only when the whole task is completely done.

## 2. Token-Efficiency Rules (Snapshot & Batch First)

- **Batch related actions into one `ego-browser nodejs` script**: Combine navigation/tab check + UI clicks + settings selection + prompt fill + reading the live credit readout into a single script invocation.
- **Prefer `page.snapshot()` and targeted `page.evaluate()` over screenshots**:
  - Do NOT call `page.screenshot()` on every intermediate step.
  - Read credit balance, model name, aspect ratio, and generation completion status via `page.snapshot()` or concise `page.evaluate()` DOM queries.
  - Take a `page.screenshot()` (or inspect downloaded files via `read_file`) ONLY when visual quality inspection of generated images/frames is needed or when DOM semantics are missing.

## 3. Canonical Entry URL & Fast-Path Auth Check

- Always navigate directly to **`https://flow.google.com/`**. Never use legacy `https://labs.google/fx/tools/flow` redirect URLs.
- Verify signed-in state from `page.snapshot()` / `page.url()`:
  - **Signed in**: URL stays on `https://flow.google.com/...` and snapshot shows `Account details` (or avatar), `+ New project` (`+ 新建项目`), or existing project cards, with no `Sign in` (`登录`) button. Proceed immediately.
  - **Needs login / CAPTCHA**: If redirected to `accounts.google.com` or showing `Sign in` / anti-bot verification, call `await task.handOff()`, stop, and ask the user to sign in inside Ego Lite, then resume with `takeOverTaskSpace(SPACE_ID)`.

## 4. Direct Local Uploads & Downloads

- **Uploads**: Pass **absolute local paths** directly to `page.setInputFiles(...)` or `chooser.setFiles(...)` via `page.waitForFileChooser()`. No need to stage files into `browser_sandbox/uploads/`.
- **Downloads**: Arm `const dlPromise = page.waitForEvent("download", { timeout: 60_000 })` before clicking the download option, then call `await dl.saveAs("/abs/path/to/workspace/output.ext")` directly to the target workspace folder.
- **0-Credit Download Default**: On image/video download menus, default to `1K 原始尺寸` / `Original size` (images) or `1080p Upscaled` / `720p Original size` (videos), which cost `0` credits. Never click `4K Upscaled` (`50 credits`) without explicit user approval.

## 5. Autonomy Mode (`checkpoint` vs `auto`) & Safety

- **`checkpoint` mode (default)**: Configure Mode, Model, Aspect Ratio, Output Count, attach references, fill the prompt, and read the exact live credit readout (`Generating will use <N> credits` / `生成将消耗 <N> 个点数`). Then pause (keeping the tab via `finish({ keep: [page.label] })`) and ask the user to confirm before clicking `Start generation` / `开始生成`.
- **`auto` mode**: Activated when the user says `"auto mode"`, `"full-auto"`, `"自动模式"`, `"直接生成不用问"`, etc. Execute end-to-end without pausing before `Start generation`.
- **Hard pauses (both modes)**: Always `handOff()` and ask the user if Google Sign-In, CAPTCHA, or `PAYMENT_REQUIRED` / credit exhaustion occurs.
