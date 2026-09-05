--- @since 25.3.0

local get_hovered = ya.sync(function()
	local h = cx.active.current.hovered
	return h and tostring(h.url) or nil
end)

local get_cwd = ya.sync(function()
	return tostring(cx.active.current.cwd)
end)

-- Returns list of selected file paths, or {hovered} if nothing selected
local get_targets = ya.sync(function()
	local tab = cx.active
	local paths = {}
	for _, u in pairs(tab.selected) do
		paths[#paths + 1] = tostring(u)
	end
	if #paths > 0 then return paths end
	local h = tab.current.hovered
	return h and { tostring(h.url) } or {}
end)

local function notify(title, content, level)
	ya.notify({
		title = title,
		content = content,
		timeout = 5,
		level = level or "info",
	})
end

-- Run chezmoi command silently, show result as notification
local function run_action(label, args)
	local output, err = Command("chezmoi")
		:arg(args)
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:output()

	if not output then
		return notify("Chezmoi", "Failed to run: " .. tostring(err), "error")
	end

	if output.status.success then
		local msg = output.stdout ~= "" and output.stdout or (label .. " completed")
		notify("Chezmoi", msg, "info")
	else
		local msg = output.stderr ~= "" and output.stderr or output.stdout
		notify("Chezmoi", label .. " failed:\n" .. msg, "error")
	end
end

-- Run chezmoi command interactively (edit, diff, status)
local function run_interactive(args)
	local permit = ui.hide()
	local child, err = Command("chezmoi")
		:arg(args)
		:stdin(Command.INHERIT)
		:stdout(Command.INHERIT)
		:stderr(Command.INHERIT)
		:spawn()

	if child then
		child:wait()
	elseif err then
		notify("Chezmoi", "Failed to spawn: " .. tostring(err), "error")
	end

	if permit then permit:drop() end
end

-- Run chezmoi command and pipe output to less
local function run_paged(args)
	local parts = {}
	for _, a in ipairs(args) do
		if a:find("[%s'\"\\]") then
			parts[#parts + 1] = "'" .. a:gsub("'", "'\\''") .. "'"
		else
			parts[#parts + 1] = a
		end
	end

	local permit = ui.hide()
	local child, err = Command("sh")
		:arg({ "-c", "chezmoi " .. table.concat(parts, " ") .. " | less -R" })
		:stdin(Command.INHERIT)
		:stdout(Command.INHERIT)
		:stderr(Command.INHERIT)
		:spawn()

	if child then
		child:wait()
	elseif err then
		notify("Chezmoi", "Failed to spawn: " .. tostring(err), "error")
	end

	if permit then permit:drop() end
end

-- Run chezmoi list command piped through fzf, navigate to selection
local function run_fzf(subcmd, extra_args)
	local cmd = "chezmoi " .. subcmd
	if extra_args then
		cmd = cmd .. " " .. extra_args
	end
	cmd = cmd .. " | fzf --prompt='chezmoi " .. subcmd .. " > '"

	local permit = ui.hide()
	local child, err = Command("sh")
		:arg({ "-c", cmd })
		:stdin(Command.INHERIT)
		:stdout(Command.PIPED)
		:stderr(Command.INHERIT)
		:spawn()

	local output
	if child then
		output, err = child:wait_with_output()
	end

	if permit then permit:drop() end

	if not output then return end
	if not output.status.success and output.status.code ~= 130 then
		return notify("Chezmoi", "fzf exited with code " .. tostring(output.status.code), "error")
	end

	local selected = output.stdout:gsub("\n$", "")
	if selected == "" then return end

	-- Resolve to absolute path
	local home = os.getenv("HOME") or ""
	local url
	if selected:sub(1, 1) == "/" then
		url = Url(selected)
	elseif selected:sub(1, 2) == "~/" then
		url = Url(home .. selected:sub(2))
	else
		url = Url(home .. "/" .. selected)
	end

	local cha = fs.cha(url)
	if cha then
		ya.emit(cha.is_dir and "cd" or "reveal", { url, raw = true })
	else
		ya.emit("reveal", { url, raw = true })
	end
end

local function entry(_, job)
	local action = job.args[1] or "status"

	if action == "add" then
		local targets = get_targets()
		if #targets == 0 then return notify("Chezmoi", "No files selected", "warn") end
		local args = { "add" }
		for _, p in ipairs(targets) do args[#args + 1] = p end
		run_action("add", args)

	elseif action == "add-encrypt" then
		local targets = get_targets()
		if #targets == 0 then return notify("Chezmoi", "No files selected", "warn") end
		local args = { "add", "--encrypt" }
		for _, p in ipairs(targets) do args[#args + 1] = p end
		run_action("add --encrypt", args)

	elseif action == "re-add" then
		local targets = get_targets()
		if #targets == 0 then return notify("Chezmoi", "No files selected", "warn") end
		local args = { "re-add" }
		for _, p in ipairs(targets) do args[#args + 1] = p end
		run_action("re-add", args)

	elseif action == "edit" then
		local hovered = get_hovered()
		if not hovered then return notify("Chezmoi", "No file hovered", "warn") end
		run_interactive({ "edit", hovered })

	elseif action == "diff" then
		local hovered = get_hovered()
		if hovered then
			run_paged({ "diff", hovered })
		else
			run_paged({ "diff" })
		end

	elseif action == "apply" then
		local targets = get_targets()
		if #targets == 0 then return notify("Chezmoi", "No files selected", "warn") end
		local args = { "apply" }
		for _, p in ipairs(targets) do args[#args + 1] = p end
		run_action("apply", args)

	elseif action == "status" then
		run_paged({ "status" })

	elseif action == "managed" then
		run_fzf("managed")

	elseif action == "unmanaged" then
		run_fzf("unmanaged", ".")

	elseif action == "forget" then
		local targets = get_targets()
		if #targets == 0 then return notify("Chezmoi", "No files selected", "warn") end
		local args = { "forget" }
		for _, p in ipairs(targets) do args[#args + 1] = p end
		run_interactive(args)

	elseif action == "goto" then
		local cwd = get_cwd()
		local root_out = Command("chezmoi"):arg("source-path"):stdout(Command.PIPED):stderr(Command.PIPED):output()
		local source_root = root_out and root_out.stdout:gsub("\n$", "") or ""
		local in_source = source_root ~= "" and cwd:sub(1, #source_root) == source_root
		local subcmd = in_source and "target-path" or "source-path"
		local output, err = Command("chezmoi")
			:arg({ subcmd, cwd })
			:stdout(Command.PIPED)
			:stderr(Command.PIPED)
			:output()
		if not output then
			return notify("Chezmoi", "Failed to run: " .. tostring(err), "error")
		end
		if not output.status.success then
			local msg = output.stderr ~= "" and output.stderr or "Not managed by chezmoi"
			return notify("Chezmoi", msg, "error")
		end
		local target = output.stdout:gsub("\n$", "")
		if target == "" then return end
		ya.emit("tab_create", { Url(target) })
	end
end

return { entry = entry }
