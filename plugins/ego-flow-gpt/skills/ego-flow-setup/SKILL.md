---
name: ego-flow-setup
description: Check or troubleshoot the local EGO Lite connection for Google Flow in ChatGPT Work or Codex. Use for plugin setup, connection checks, or local-browser errors; not for generating images or videos.
---

# EGO Flow Setup

Read [the shared operating contract](references/operating.md) before browser work. Image and video skills explicitly load that same contract; do not rely on a repository AGENTS file being auto-loaded after plugin installation.

## Connection check

1. Confirm this conversation can execute commands on the user's intended local computer. A local-looking path in a cloud shell is not proof of access. If the local executor is absent, stop and explain that this desktop-only plugin needs a locally running conversation. Do not invent a remote EGO bridge or switch to a different browser.
2. Run `ego-browser skill`. Read the complete installed guide through its end marker. This is the runtime API source of truth. If the command is missing, explain that EGO Lite must be installed first. Do not install, upgrade, modify permissions or switch profiles without approval.
3. Run an actual read-only EGO browser round: create or resume this goal's TaskSpace, open `https://flow.google.com/`, print the space ID, page label, current URL and a compact snapshot. Use [browser round examples](references/browser-rounds.md) only where they agree with the installed guide.
4. Distinguish a reachable marketing page from an authenticated workspace. Workspace controls and the user's projects are stronger evidence than the URL alone. A page that lacks a Sign in button is not sufficient proof of login.
5. Report what was observed: local runtime reachable, Flow page reachable, authenticated or not yet verified, and whether credits/settings were actually visible. Setup never creates a project, uploads user files or clicks Generate.

For a setup-only check that reaches an introduction/login page, report the limit and finish the agent-created diagnostic space; do not force a sign-in detour. For a requested generation that requires login, use the shared handoff rules and wait for the user in the same space.

If execution is blocked by the host's permissions, use that host's supported approval flow, limited to the browser command. Do not add Antigravity-specific execution flags or grant yourself broader access. After a successful connectivity check, a later real task still needs its own live settings and cost check.
