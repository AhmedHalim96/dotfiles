import os
import subprocess
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()
qtile_path = os.path.expanduser('~/.config/qtile')

keys = [
    # Switch between windows
    Key([alt], "Tab",
        lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows 
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"),

    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Grow windows
    Key([mod], "h",
        lazy.layout.shrink_main(),
        desc="Shrink Master"),

    Key([mod], "l",
        lazy.layout.grow_main(),
        desc="Grow Master"),

    Key([mod], "j",
        lazy.layout.shrink(),
        desc="Shrink secondary"),

    Key([mod], "k",
        lazy.layout.grow(),
        desc="Grow Secondary"),
    
    # Window keybindings
    Key([mod, "control"], "space",
        lazy.window.toggle_floating(),
        desc="Toggle floating"),

    Key([mod], "m",
        lazy.window.toggle_maximize(),
        desc="Toggle maximize"),

    Key([mod], "n",
        lazy.window.toggle_minimize(),
        desc="Toggle minimize"),

    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen"),

    Key([mod], "q",
        lazy.window.kill(),
        desc="Kill focused window"),

    # Toggle between different layouts as defined below
    Key([mod], "space",
        lazy.next_layout(),
        desc="Next layouts"),

    # Qtile control
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart Qtile"),

    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"),

    # Programs
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"),

    Key([mod], "r",
        lazy.spawn("dmenu_run_history -f -i -p 'Run: '"),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "b",
        lazy.spawn("brave-browser"),
        desc="Open Default Browser"),

    Key([mod], "c",
        lazy.spawn("copyq toggle"),
        desc="Open copyq prompt"),

    Key([mod], "tab",
        lazy.spawn("rofi -show"),
        desc="rofi window"),

    Key([mod], "s",
        lazy.spawn("smplayer"),
        desc="Open smplayer"),

    Key([mod], "e",
        lazy.spawn("nautilus"),
        desc="Open nautilus"),

    Key([mod, 'shift'], "e",
        lazy.spawn("lf_fm"),
        desc="Open lf"),

    Key([mod], "comma",
        lazy.spawn("codium " + qtile_path),
        desc="Open qtile config"),

    Key([mod, "shift"], "comma",
        lazy.spawn("dmconf"),
        desc="Open dmconf"),

    # Media Keys
    Key([mod, "control"], "Up",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"),
        desc="Raise volume"),
    
    Key([mod, "control"], "Down",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),
        desc="lower volume"),

    Key([], "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause"),

    Key([], "XF86AudioNext",
        lazy.spawn("playerctl next"),
        desc="Next track"),
    
    Key([], "XF86AudioPrev",
        lazy.spawn("playerctl previous"),
        desc="Previous track"),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(margin=5, ratio=.55, new_client_position='bottom'),
    # layout.Max(),
    # layout.Floating()
    # layout.Columns(num_columns=2, insert_position=1, margin=5),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(border_focus_stack='#d75f5f'),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Monospace',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                # widget.WindowName(),
                widget.WindowTabs(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.CurrentLayout(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position(),
        start=lazy.window.get_position()),
    Drag([mod, "control"], "Button1", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Albert'),
    Match(wm_class='copyq'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([autostart_script])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
