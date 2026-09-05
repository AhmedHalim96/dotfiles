# chezmoi.yazi

A [Yazi](https://github.com/sxyazi/yazi) plugin for managing dotfiles with [chezmoi](https://www.chezmoi.io/) directly from your file manager.

> [!NOTE]
> Requires Yazi v25.3+ and [chezmoi](https://www.chezmoi.io/) installed.

## Features

- Add, re-add, and remove files from chezmoi tracking
- Edit chezmoi source files in `$EDITOR`
- Diff source vs target with paged output
- Apply chezmoi changes to target files
- View chezmoi status
- Browse managed/unmanaged files with fzf
- Jump between source and target directories (bidirectional)
- Works with multi-select (selected files) or single hovered file

## Requirements

- [chezmoi](https://www.chezmoi.io/)
- [fzf](https://github.com/junegunn/fzf) (for `managed`/`unmanaged` actions)
- `less` (for paged output)

## Installation

```sh
ya pkg add heretic-tripto/chezmoi
```

or

```sh
# Linux/macOS
git clone https://github.com/heretic-tripto/chezmoi.yazi.git ~/.config/yazi/plugins/chezmoi.yazi

# Windows
git clone https://github.com/heretic-tripto/chezmoi.yazi.git %AppData%\yazi\config\plugins\chezmoi.yazi
```

## Setup

No `init.lua` configuration is needed. Just add the keybindings below.

## Keymap

Add this to your `keymap.toml`:

```toml
[[mgr.prepend_keymap]]
on   = [ "C", "a" ]
run  = "plugin chezmoi add"
desc = "Chezmoi add"

[[mgr.prepend_keymap]]
on   = [ "C", "A" ]
run  = "plugin chezmoi add-encrypt"
desc = "Chezmoi add (encrypted)"

[[mgr.prepend_keymap]]
on   = [ "C", "r" ]
run  = "plugin chezmoi re-add"
desc = "Chezmoi re-add"

[[mgr.prepend_keymap]]
on   = [ "C", "e" ]
run  = "plugin chezmoi edit"
desc = "Chezmoi edit source"

[[mgr.prepend_keymap]]
on   = [ "C", "d" ]
run  = "plugin chezmoi diff"
desc = "Chezmoi diff"

[[mgr.prepend_keymap]]
on   = [ "C", "p" ]
run  = "plugin chezmoi apply"
desc = "Chezmoi apply"

[[mgr.prepend_keymap]]
on   = [ "C", "s" ]
run  = "plugin chezmoi status"
desc = "Chezmoi status"

[[mgr.prepend_keymap]]
on   = [ "C", "m" ]
run  = "plugin chezmoi managed"
desc = "Chezmoi managed (fzf)"

[[mgr.prepend_keymap]]
on   = [ "C", "u" ]
run  = "plugin chezmoi unmanaged"
desc = "Chezmoi unmanaged (fzf)"

[[mgr.prepend_keymap]]
on   = [ "C", "f" ]
run  = "plugin chezmoi forget"
desc = "Chezmoi forget"

[[mgr.prepend_keymap]]
on   = [ "C", "g" ]
run  = "plugin chezmoi goto"
desc = "Chezmoi goto source/target"
```

All keymaps use `C` as a chord prefix — press `C` then the action key. Adjust to your preference.

## Actions

| Action | Behavior | Target |
|--------|----------|--------|
| `add` | Add file to chezmoi | selected / hovered |
| `add-encrypt` | Add with encryption | selected / hovered |
| `re-add` | Update source from target | selected / hovered |
| `edit` | Edit source in `$EDITOR` | hovered |
| `diff` | Diff source vs target (paged) | hovered or all |
| `apply` | Apply source to target | selected / hovered |
| `status` | Show chezmoi status (paged) | all |
| `managed` | Browse managed files with fzf | all |
| `unmanaged` | Browse unmanaged files with fzf | cwd |
| `forget` | Remove from chezmoi (interactive) | selected / hovered |
| `goto` | Open source/target in new tab | cwd |

The `goto` action is bidirectional — if you're in a target directory (e.g. `~/.config/fish/`), it opens the chezmoi source. If you're already in the source directory, it opens the target.

## License

MIT
