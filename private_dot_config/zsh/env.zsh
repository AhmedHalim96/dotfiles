#Enviroment Variables
#!/bin/zsh
#
export XDG_DATA_HOME=$HOME/.local/share
export XDG_STATE_HOME=$HOME/.local/state
export XDG_CACHE_HOME=$HOME/.cache
export XDG_PICTURE_DIR=$HOME/Pictures/Screenshots
export CARGO_HOME="$XDG_DATA_HOME"/cargo
export GNUPGHOME="$XDG_DATA_HOME"/gnupg
export WINEPREFIX="/mnt/Data/Games/wine/"
export LS_COLORS="$(vivid generate snazzy)"
export EDITOR=nvim
export VISUAl=nvim
export BROWSER=floorp
export FILE_MANAGER=/usr/bin/nemo
export TERMINAL_FM="spf"
export GITSTATUS_LOG_LEVEL=DEBUG
export TERMINAL="kitty"
export MANPAGER="nvim +Man!"
export ZVM_VI_EDITOR=nvim
#export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
export HISTDB_FILE="$HOME/.cache/zshhistory"
#misc
#export LC_ALL="en_US.UTF-8"
#export LANG="en_US.UTF-8"
#export LOCALE_ARCHIVE="/nix/store/h1kxm30h8y5dr1xkfr4w38g7fg2xw1zq-glibc-locales-2.35-163/lib/locale/locale-archive"
export NO_AT_BRIDGE=1
export XDG_CONFIG_HOME="$HOME/.config"
export GTK_SILENT=1
export RANGER_LOAD_DEFAULT_RC=false
#export FZF_DEFAULT_COMMAND='fd --type file --follow  --exclude .git,node_modules --color=always'
#export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export GENCOMPL_FPATH=$HOME/.zsh/completions
#export GTK_THEME=Sweet-Dark
#export GTK_ICON_THEME=Papirus-Dark
#export all_proxy="socks5://127.0.0.1:9050" #Proxy
#export _JAVA_AWT_WM_NONREPARENTING=1
#export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on'
export GAMES_HOME="/mnt/Data/Games"
export GENCOMPL_FPATH=~/.config/zsh/zsh_functions
export PF_SEP=""
export PF_INFO="ascii title os kernel wm shell uptime pkgs memory"
