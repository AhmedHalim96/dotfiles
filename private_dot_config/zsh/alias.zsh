#!/bin/zsh

############################################################################
### Aliases
############################################################################


# navigation
alias ..='cd ..'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../..'
alias .5='cd ../../../..'
alias .6='cd ../../../../..'

# pnpm Aliases
alias pn='pnpm'
alias px='pnpx'
alias pi='pnpm install'
alias pa='pnpm add'
alias pr='pnpm run'
alias pd="pnpm dev"


# Changing "ls" to "exa"
alias exa="eza"
alias l='exa --icons --color=always --group-directories-first' # my preferred listing
alias ls='exa --icons -l --color=always --group-directories-first' # my preferred listing
alias la='exa --icons -a --color=always --group-directories-first'  # all files and dirs
alias ll='exa --icons -al --color=always --group-directories-first'  # long format
alias lt='exa --icons -aT --color=always --group-directories-first' # tree listing
alias l.='exa -a | rg "^\."'

# adding flags
alias cp="cp -iv"                         # confirm before overwriting something and verbose
alias mv="mv -iv"                         # confirm before overwriting something and verbose
alias rm="rm -iv"                         # rm verbose
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias tree='tree -C'                      # Colorization always on
alias grep='grep --color=auto'
alias fgrep='fgrp --color=auto'
alias egrep='egrep --color=auto'
alias dolphin='dolphin -stylesheet /home/ahmed/.config/dolphin/style.qss'
alias f="fd"
alias fa="fd -uu"
alias rg="rg -i"
alias mkdir="mkdir -pv"                   # create parent directories
alias part_uuid="lsblk -dno PARTUUID"
alias lsblk="lsblk -f"



# youtube-dl
alias ytdl="/usr/bin/yt-dlp -P ~/Downloads/yt-dlp"
alias ytdl-aria="ytdl --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M'"
alias ytdl-mp3="ytdl --extract-audio --embed-metadata --audio-format mp3"


ytdl-list () {
  # if there's no file argument open editor and let the user paste URLs then use the list file
  if [ $# -eq 0 ]; then
    $EDITOR ~/.cache/ytdl-list
    ytdl -a ~/.cache/ytdl-list -i
    notify-send "Youtube-dl" "Download completed"
    return
  fi
  ytdl -a ~/.cache/ytdl-list "$@" -i
  notify-send "Youtube-dl" "Download completed"
}

# gallery-dl
#alias gdl="gallery-dl"
#alias gdlw="gdl -o downloader.http.headers.User-Agent=Wget/1.21.1"
#alias gdl.="gdl -o directory='' -d ."


gdl-list() {
  rm -f ~/.cache/gallery-dl/url_list
  $EDITOR ~/.cache/gallery-dl/url_list
  gdl. -i ~/.cache/gallery-dl/url_list
  notify-send "Gallery-dl" "Download completed"
}



# mpv
alias mpv="mpv"
alias mpv-360="mpv --ytdl-format='bestvideo[height<=?360]+bestaudio/best[height<=?360]'"
alias mpv-480="mpv --ytdl-format='bestvideo[height<=?360]+bestaudio/best[height<=?480]'"
alias mpv-720="mpv --ytdl-format='bestvideo[height<=?720]+bestaudio/best[height<=?720]'"
alias mpv-a="mpv-360 --no-video"

# git aliases
alias status="git status"
alias add="git add"
alias add.="git add ."
alias commit="git commit -m"
alias log="git log"
alias pull="git pull"
alias push="git push"
alias clone="git clone"
alias ginit="git init"
alias checkout="git checkout"
alias checkout-b="checkout -b"
alias branch="git branch"
alias branch-d="branch -d"
alias stash="git stash"
alias merge="git merge"
alias countCommits="git log | grep "commit" | wc -l"

# Dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias .f="dotfiles"
alias .fs=".f status"
alias .fa=".f add"
alias .faa=".f add -u"
alias .fc=".f commit -m"
alias .fca=".f commit -a -m"


#Networking
alias myip="curl ipinfo.io/ip"
alias ports="netstat -tulanp"

#replacing tools
alias cat="bat"
alias du="dust"
alias ping="prettyping --nolegend"
alias neofetch="fastfetch"
alias nvm="fnm"
alias htop="btop"
alias pip="uv pip"
alias docker="podman"


# npm
alias npmd="npm run dev"
alias npmb="npm run build"
alias npmbs="npm run build && npm run start"
alias npms="npm run start"

# bluetooth
alias bt="bluetoothctl"
alias btc="bluetoothctl connect"
alias btd="bluetoothctl disconnect"
alias btl="bluetoothctl devices Paired"
alias bts="bluetoothctl scan on"
alias bti="bluetoothctl info"
alias btr="bluetoothctl remove"

# zellij
alias zj="zellij"
alias zjl="zellij ls"
alias zjn="zellij new-session"
alias zjattach="zellij attach"
alias zja="zellij a"

# Misc
##
alias c='clear' # clear terminal
alias xx="exit" # exit Shell
alias rr="exec zsh" # restart Shell
alias .files="GIT_DIR=~/dotfiles/ GIT_WORK_TREE=~ tig status"
alias icat="kitty +kitten icat"
alias kmn="viu ~/.local/share/dead.png"
alias pa="php artisan"
alias pa-serv="pa serve --host=192.168.1.111 --port=8000"
alias rn="npx react-native"
alias rna="npx react-native run-android"
alias srt="python3 '/home/ahmed/.local/share/nemo/scripts/OpenSubtitlesDownload.py'"
alias pyx="pyenv exec"
alias gget="python3 ~/git_repos/gallery_get/gallery_get.py"
alias rip="java -jar /mnt/Data/.NotPorn/ripme-1.7.93-jar-with-dependencies.jar -u"
alias d="devour"
alias ka="killall"
alias jn="jupyter-notebook --notebook-dir ~/Projects/Jupyter"
alias v="nvim"
alias b64="base64 <<<"
alias b64-d="base64 -d <<<"
alias h="history 0 | bat"
alias wmclass="xprop WM_CLASS"
alias wmname="xprop WM_NAME"
alias proton="STEAM_COMPAT_DATA_PATH=~/.proton/ /home/ahmed/.steam/root/compatibilitytools.d/Proton-6.10-GE-1/proton run"
alias thumbs="vcsi -t -g 3x5 -w 5760"
alias vw="nvim -c ':VimwikiIndex'"
alias vd="nvim -c ':VimwikiMakeDiaryNote'"
alias vdi="nvim -c ':Diary'"
alias pg="pgrep"
alias pk="pkill"
alias lyrics="lyricsmpris"
alias gamerun="prime-run mangohud gamemoderun"
alias pwdc="pwd | wl-copy"


# systemctl
alias sc="sudo systemctl"
alias sci='sc start'
alias scr='sc restart'
alias scs='sc stop'
alias scst='systemctl status'
alias sce="sc enable --now"
alias scd="sc disable --now"
alias scu="systemctl --user"
alias scur="scu restart"
alias scud="scu disable --now"
alias scue="scu enable --now"
alias scus="scu status"
alias scud="scu disable --now"
alias scue="scu enable --now"
alias scust="scu status"
alias scus="scu stop"
alias scui="scu start"

#alias radioactive="venv/bin/radioactive"
# Chezmoi
alias cz='chezmoi'
alias czi='chezmoi init'         # Initialize a new chezmoi repo
alias cza='chezmoi apply'       # Sync changes TO your home directory
alias cze='chezmoi edit'        # Edit a managed file (automatically applies on save)
alias czs='chezmoi status'      # See what's out of sync
alias czd='chezmoi diff'        # See exactly what changes will be made
alias czadd='chezmoi add'           # Add a new file to chezmoi
alias czat='chezmoi add --template' # Add a file and turn it into a template immediately
alias czm='chezmoi managed'         # List all files currently managed by chezmoi
alias czcd='cd $(chezmoi source-path)' # Jump straight to the local repo
alias czup='chezmoi update'            # Pull latest from Git and apply changes
alias czp='czcd && git add . && git commit -m "update dotfiles" && git push && cd -'
alias czn='chezmoi apply --dry-run --verbose' # "What would happen if I ran this?"
alias czlog='git -C $(chezmoi source-path) log --oneline --graph' # See your config history


# Sudo Aliases
alias tuxcut-i="sudo systemctl start tuxcutd"
alias tuxcut-s="sudo systemctl stop tuxcutd"
alias tor-restart="sudo systemctl restart tor"
alias tor-stop="sudo systemctl stop tor"
alias xammp+='sudo systemctl stop apache2 && sudo systemctl stop mysql && sudo /opt/lampp/manager-linux-x64.run'
alias xammp='sudo /opt/lampp/manager-linux-x64.run'
alias vhosts='vim /opt/lampp/etc/extra/httpd-vhosts.conf'
alias lf-sudo="sudo ~/.local/bin/lf"
alias apt="sudo apt"
alias nala="sudo nala"
alias dnf="sudo dnf"
alias pacman="sudo pacman"
alias system-update="nala upgrade -y &&  nala autoremove -y"
alias waydroid-mount="sudo mount --bind ~/waydroid/Download ~/.local/share/waydroid/data/media/0/Download"
alias timeshift="sudo timeshift"

## pacman and yay
# Update everything (Repos + AUR)
alias yolo='yay -Syu'
# The "Safe" Update: Refresh keys first (helps if you haven't updated in weeks)
alias yup='pacman -Sy archlinux-keyring && yay -Syu'
# Just download, don't install (Manual trigger for your prefetching)
alias yfetch='yay -Syuw --noconfirm'
# Search for a package in both Repos and AUR
alias ys='yay -Ss'
# Install a package
alias yi='SKIP_AUTOSNAP=1 yay -S --needed'
# Get detailed info on a package
alias yinfo='SKIP_AUTOSNAP=1 yay -Si'
# Remove a package and its unneeded dependencies
alias yr='yay -Rs'
# Clean the cache: keeps only the last 3 versions of installed packages (requires pacman-contrib)
alias yclean='sudo paccache -rk3'
# Remove "orphans" (packages installed as dependencies but no longer needed)
alias yorph='pacman -Rns $(pacman -Qtdq)'
# List the last 20 packages installed
alias yhist='expac --timefmt="%Y-%m-%d %T" "%l\t%n" | sort | tail -n 20'
# List all installed AUR packages
alias yaur='yay -Qm'
alias ycheck='yay -Qu'

## docker

alias dps='docker ps --format "ID\t{{.ID}}\nNAME\t{{.Names}}\nImage\t{{.Image}}\nPORTS\t{{.Ports}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.CreatedAt}}\nSTATUS\t{{.Status}}\n"'
alias drm='docker rm $(docker ps -aq)'
alias dkill='docker kill $(docker ps -q)'
alias dpull='docker pull'


############################################################################
### Functions
############################################################################

### ARCHIVE EXTRACTION
# usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   unzstd $1    ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}




browser-test(){
  cd ~/code/playwright
  URL=$2 npm run test:$1
}


FM="yazi" #yazi or spf or lf or ranger

jj() {
  if [ "$1" != "" ]; then
    if [ -e "$1" ]; then
      "$FM" "$1"
    else
	    result="$(zoxide query --exclude $PWD $1 | sed 's/\\/\\\\/g;s/"/\\"/g')"
      "$FM" "$result"
    fi
  else
    "$FM" "$PWD"
  fi
	return $?
}


lf () {
 jj $@
}
