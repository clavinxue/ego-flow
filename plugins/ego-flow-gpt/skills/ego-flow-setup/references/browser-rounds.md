# Browser Round Examples

Read the installed `ego-browser skill` first. The examples below match the locally checked v2.2.1 guide, but the installed guide takes precedence. They are scaffolds: never execute a selector or ID without current evidence.

## Begin or resume

Run the following through `ego-browser nodejs` using the host's authorized local command tool. Print only concise metadata, never account secrets. Pass absolute paths explicitly; the nodejs process does not inherit shell exports.

```js
const SPACE_ID = null; // replace only with the observed ID for this user goal
const entry = SPACE_ID === null
  ? undefined
  : (await listTaskSpaces()).find(s => s.id === SPACE_ID);
const task = !entry
  ? await taskSpace("Google Flow project")
  : entry.ownership === "user"
    ? await claimTaskSpace(SPACE_ID)
    : entry.ownership === "agentDelegatedToUser"
      ? await takeOverTaskSpace(SPACE_ID) // only after user's confirmation
      : await taskSpace(SPACE_ID);
let page = (await task.pages())[0];
if (!page) {
  const tab = (await task.tabs())[0];
  if (!tab) throw new Error("No existing page; inspect the runtime guide");
  page = await task.adopt(tab.page);
}
if (SPACE_ID === null) await page.goto("https://flow.google.com/");
console.log({taskSpaceId: task.spaceId, page: page.label, url: await page.url()});
console.log(await page.snapshot());
```

A missing previous space can be recreated only because it no longer exists, not to bypass a stuck or user-owned space. If the URL is a marketing or login page, do not claim that an authenticated workspace is available.

## Local upload

After identifying the upload button from a snapshot, arm the chooser, trigger it and set files in the same invocation. Replace both illustrative values with the user-authorized file and the actual selector.

```js
const chooserPromise = page.waitForFileChooser({timeout: 10000});
await page.click(observedUploadSelector, {label: "upload selected reference image"});
const chooser = await chooserPromise;
await chooser.setFiles([absoluteReferencePath]);
console.log(await page.snapshot());
```

Check thumbnail/asset attachment separately before submission. When a stable input is already observed, the installed guide also supports `page.setInputFiles`.

## Local download

Choose an option only after checking its live cost and the authorized destination. `download.path()` is round-local and not the deliverable.

```js
const downloadPromise = page.waitForEvent("download", {timeout: 60000});
await page.click(observedApprovedDownloadSelector, {label: "download approved video output"});
const download = await downloadPromise;
await download.saveAs(absoluteNewOutputPath);
console.log({savedTo: absoluteNewOutputPath, name: download.suggestedFilename()});
```

## Normal completion or checkpoint

After an earlier round has verified the result, run a separate final script using the observed TaskSpace ID. Keep only a specific prepared/result page needed for the current handoff to the user; otherwise use an empty list.

```js
const task = await taskSpace(observedSpaceId);
await task.finish({keep: requiredPageLabels});
```

Do not operate pages after `finish()` in that script. For sign-in, CAPTCHA or user control, use the installed guide's `handOff`/stop behavior instead; do not finish a delegated space.
