---
name: ego-flow-image
description: >-
  Generate images and upload local reference assets (Ingredients) in Google Flow
  (flow.google.com) using Ego Lite (ego-browser CLI). Supports Nano Banana 2.1,
  Nano Banana 2 Lite, and Nano Banana Pro, direct local file uploads, batched
  DOM configuration, exact credit checks, and 0-credit 1K downloads.
---

# Ego Flow Image (Upload References & Nano Banana Generation)

Use **Ego Lite (`ego-browser nodejs`)** to manage Google Flow projects, upload local reference images directly, and generate images with `Nano Banana` in a token-efficient, credit-safe workflow.

## Workflow

### Step 1: Resolve Space & Open/Create Project (Single Batched Script)

Run one `ego-browser nodejs` script (`BypassSandbox: true`) to:
1. Claim or create a TaskSpace (`taskSpace("google-flow")` or `claimTaskSpace(SPACE_ID)` if continuing from an earlier reply).
2. Navigate to `https://flow.google.com/` (if not already on `flow.google.com`).
3. Check `page.url()` and `page.snapshot()` for signed-in state:
   - If on `accounts.google.com` or `Sign in` / `登录` is visible, call `await task.handOff()` and ask the user to sign in.
4. Open the requested project (`/project/<id>`) or click `+ New project` (`+ 新建项目`) and rename the project title if requested.
5. Print `{ taskSpaceId, page: page.label, url: await page.url() }` and `await page.snapshot()`.

### Step 2: Upload Local Reference Images (Direct Absolute Paths)

If the user provided local reference images (`.png`, `.jpg`, `.jpeg`, `.webp`):
- Verify the local files exist first.
- In `ego-browser nodejs`, trigger the upload control (`+` -> `Upload` / `上传媒体`) using `waitForFileChooser` before clicking:
  ```js
  const chooserPromise = page.waitForFileChooser({ timeout: 10_000 });
  await page.click("...", { label: "open upload file chooser" });
  const chooser = await chooserPromise;
  await chooser.setFiles(["/abs/path/img1.jpg", "/abs/path/img2.png"]);
  ```
- Wait for the uploaded thumbnails to appear in the project/prompt bar via `waitForSelector` or `waitForFunction`, then attach them to the prompt box if not auto-attached.

### Step 3: Configure Manual Mode, Settings & Read Live Credit Cost (Batched)

In a single script:
1. Ensure **`Flow Agent` / `Flow 智能体`** toggle is **OFF** (`aria-pressed="false"`).
2. Open the Settings trigger popover in the bottom composer:
   - **Mode**: `Image` / `图片`
   - **Model**: `Nano Banana 2.1` (default), `Nano Banana 2 Lite`, or `Nano Banana Pro`
   - **Aspect Ratio**: `4:3`, `16:9`, `1:1`, `3:4`, or `9:16`
   - **Output count**: `x1`–`x4`
   - Read the live credit indicator (`Generating will use <N> credits` / `生成将消耗 <N> 个点数`).
3. Fill the prompt box (`"What do you want to create?"` / `"您希望创作什么？"`).
4. **Checkpoint check**:
   - In **`checkpoint` mode** (default): Do **NOT** click `Start generation` / `开始生成`. Run `await task.finish({ keep: [page.label] })` and report: Project URL, attached references, Model, Aspect Ratio, Output Count, and exact live credit cost. Wait for user confirmation.
   - In **`auto` mode**: Proceed directly to Step 4.

### Step 4: Generate & Download (0-Credit Original Size)

1. Click `Start generation` / `开始生成`.
2. Wait until rendering finishes (poll cleanly inside `page.waitForFunction` or bounded `waitForTimeout` loops without spamming screenshots).
3. Download candidates directly to the workspace using `page.waitForEvent("download")`:
   - Select **`1K 原始尺寸`** / **`1K Original size`** (`0 credits`). Never select `4K` / `2K` paid upscaling unless explicitly approved.
   - Save with `await download.saveAs("/abs/workspace/path/output_1.jpg")`.
4. Close or keep the space:
   - If the user may iterate further, `await task.finish({ keep: [page.label] })`.
   - If completely finished, `await task.finish({ keep: [] })`.
5. Inspect the downloaded image(s) with `read_file` and report the local file paths to the user.
