local wezterm = require 'wezterm';
return {
  font = wezterm.font("FiraCode Nerd Font", {weight="Medium", stretch="Normal", style="Normal"}),
  warn_about_missing_glyphs = false,
  font_size = 11.0,
  --line_height = 1.0,
  window_background_opacity = 0.85,
  term = "xterm-256color",  
  scrollback_lines = 3500,
  window_padding = {
    left = 10 ,
    right = 10,
    top = 0,
    bottom = 5,
  },
  window_frame = {
   font_size = 11.0,
  inactive_titlebar_bg = "#161925",
  active_titlebar_bg = "#161925",
  },

  colors = {
    foreground = "#C3C7D1",
    background = "#161925" ,
    ansi = { "#282C34","#ED254E","#71F74E","#F9DC5C","#7CB7FF","#C74DED","#00C1E5","#DCDFDC"},
    bright = { "#282C34","#ED254E","#71F74E","#F9DC5C","#7CB7FF","#C74DED","#00C1E5","#DCDFDC"},
    tab_bar = {
      background = "red",
      active_tab = {
        bg_color = "#161925",
        fg_color = "#c0c0c0",
      },
      inactive_tab = {
        bg_color = "#1b1032",
        fg_color = "#808080",
      },

      inactive_tab_hover = {
        bg_color = "#3b3052",
        fg_color = "#909090",
        italic = true,
      },

      new_tab = {
        bg_color = "#161925",
        fg_color = "#808080",

      },

      new_tab_hover = {
        bg_color = "#3b3052",
        fg_color = "#909090",
        italic = true,
      }
    }
  },
  tab_bar_at_bottom = false 
}


