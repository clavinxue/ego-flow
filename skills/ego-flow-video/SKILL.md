---
name: ego-flow-video
description: >-
  Plan storyboards and generate videos in Google Flow (Omni 1.2 Flash, Veo 3.1)
  using Ego Lite (ego-browser CLI). Supports Ingredients, Start/End Frames via
  direct local file upload, scene timeline assembly, and 0-credit 1080p export.
---

# Ego Flow Video (Storyboard, Shots & Scene Export)

Use **Ego Lite (`ego-browser nodejs`)** to plan shots, upload local keyframes/Ingredients, generate video clips (`Omni 1.2 Flash` / `Veo 3.1`), assemble scenes, and download finished videos directly into the workspace.

## UI & Prompt Calibration

- **No separate Camera Control menu**: Always write camera framing, lens, motion, and audio cues explicitly inside the prompt text.
- **Manual Mode required**: Turn **OFF** `Flow Agent` / `Flow 智能体` before configuring model, resolution, duration, and output count.
- **Two Video Types**:
  - `Ingredients` (Text-to-Video or `@handle` / attached Ingredients-to-Video)
  - `Frames` (`Start` and `End` keyframe slots — upload directly via `waitForFileChooser` with absolute local paths)
- **Scene Timeline**: Managed via left sidebar `Scenes` / `场景`, card `More options` -> `Add to scene`, and the editor at `/project/<projectId>/edit/<clipId>`.

## Workflow

### Step 1: Plan & Confirm (Optional Storyboard)

For multi-shot projects, draft a concise shot table (`S01..Sn`: Video Type, Ingredients/Frames, Model, Resolution/Length, Aspect Ratio, Prompt + Camera + Audio) and confirm `checkpoint` vs `auto` mode.

### Step 2: Configure Shot & Check Credits

In one batched `ego-browser nodejs` script (`BypassSandbox: true`):
1. Open/claim the Flow project (`https://flow.google.com/project/<id>`).
2. Switch `Flow Agent` OFF, open Settings -> **`Video`** (`视频`), set:
   - `Video type`: `Ingredients` or `Frames`
   - `Aspect ratio`: `16:9` or `9:16`
   - `Model`: e.g. `Omni 1.2 Flash` (`360p` draft / `720p` final, `Length` slider) or `Veo 3.1 - Lite [Lower Priority]` / `Veo 3.1 - Lite` (`4s` / `6s` / `8s`)
   - `Output count`: `x1`–`x4`
3. Upload any local `Start` / `End` keyframes or Ingredients via `waitForFileChooser` + `chooser.setFiles([...])`.
4. Fill prompt and read the exact live credit readout (`Generating will use <N> credits`).
5. In `checkpoint` mode: pause with `await task.finish({ keep: [page.label] })` and ask the user to confirm the credit cost before clicking `Start generation`.

### Step 3: Generate, Assemble & Export

1. Click `Start generation` and wait for the clip(s) to finish rendering (use `page.waitForFunction` / bounded checks via DOM rather than repeated screenshots).
2. Visually verify the best take with one `screenshot()` or thumbnail check if needed.
3. For multi-shot assembly: add selected clips via `Add to scene`, open the Scene Editor, verify sequence, and export.
4. Download via `page.waitForEvent("download")`:
   - Default to **`1080p Upscaled`** or **`720p Original size`** (`0 credits`). Confirm first before selecting `4K Upscaled · 50 credits`.
   - Call `await download.saveAs("/abs/workspace/path/shot.mp4")`.
5. Finish with `await task.finish({ keep: [page.label] })` (if iterating) or `keep: []` (if done).
