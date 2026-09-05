require("zoxide"):setup({
	update_db = true,
})

function Linemode:size_and_mtime()
	local time = math.floor(self._file.cha.mtime or 0)
	if time == 0 then
		time = ""
	elseif os.date("%Y", time) == os.date("%Y") then
		time = os.date("%b %d %H:%M", time)
	else
		time = os.date("%b %d  %Y", time)
	end

	local size = self._file:size()
	return string.format("%s %s", size and ya.readable_size(size) or "-", time)
end

Status:children_add(function()
	local h = cx.active.current.hovered
	if not h then
		return ui.Line({})
	end

	return ui.Line({
		ui.Span(os.date("%Y-%m-%d %H:%M", math.floor(h.cha.mtime or 0))):fg("blue"),
		ui.Span(" "),
	})
end, 500, Status.RIGHT)

-- Save selected files to a global state file
function sync_yank()
    local selected = cx.active.selected
    if #selected == 0 then
        selected = { cx.active.current.hovered.url }
    end

    local paths = ""
    for _, url in pairs(selected) do
        paths = paths .. tostring(url) .. "\n"
    end

    -- Write to a temp file (like /tmp/yazi-yank)
    local f = io.open("/tmp/yazi-yank", "w")
    if f then
        f:write(paths)
        f:close()
    end
end
