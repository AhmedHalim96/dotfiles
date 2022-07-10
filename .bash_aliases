# ~/.bash_aliases: executed by bash(1) for non-login shells.
# Bash Aliases


# navigation
alias ..='cd ..'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../..'
alias .5='cd ../../../..'
alias .6='cd ../../../../..'


# Changing "ls" to "exa"
alias l='exa --color=always --group-directories-first' # my preferred listing
alias ls='exa -l --color=always --group-directories-first' # my preferred listing
alias la='exa -a --color=always --group-directories-first'  # all files and dirs
alias ll='exa -al --color=always --group-directories-first'  # long format
alias lt='exa -aT --color=always --group-directories-first' # tree listing
alias l.='exa -a | egrep "^\."'


# adding flags
alias cp="cp -i"                          # confirm before overwriting something
alias mv="mv -i"                          # confirm before overwriting something
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias tree='tree -C'                      # Colorization always on

# youtube-dl
alias ydl="youtube-dl"
alias ydl-d="youtube-dl --output '/home/ahmed/Downloads/%(title)s_%(id)s.%(ext)s'"
alias ydl-p="youtube-dl --output '/mnt/Data/.NotPorn/ydl/%(title)s_%(id)s.%(ext)s'"
alias ydl-mp3="ydl-d --extract-audio --audio-format mp3"
#alias yta-aac="youtube-dl --extract-audio --audio-format aac "
#alias yta-best="youtube-dl --extract-audio --audio-format best "
#alias yta-flac="youtube-dl --extract-audio --audio-format flac "
#alias yta-m4a="youtube-dl --extract-audio --audio-format m4a "
#alias yta-mp3="youtube-dl --extract-audio --audio-format mp3 "
#alias yta-opus="youtube-dl --extract-audio --audio-format opus "
#alias yta-vorbis="youtube-dl --extract-audio --audio-format vorbis "
#alias yta-wav="youtube-dl --extract-audio --audio-format wav "
#alias ytv-best="youtube-dl -f bestvideo+bestaudio "


# git aliases
alias status="git status"
alias add="git add"
alias add.="git add ."
alias commit="git commit -m"
alias log="git log"
alias pull="git pull"
alias push="git push origin"
alias clone="git clone"
alias ginit="git init"
alias checkout="git checkout"
alias new-branch="checkout -b"
alias branch="git branch"
alias del-branch="branch -d"



# Custom aliases
alias c='clear'
alias gedit="xed"

#alias pornpy="python3 /home/ahmed/PycharmProjects/Scripts/pornGenrator.py"
alias pa="php artisan"
#alias code="code-insiders"
#alias ls="ls -l"
alias srt="python3 '/home/ahmed/.local/share/nemo/scripts/OpenSubtitlesDownload.py'"

# Directories
alias AJ="nemo /mnt/Data/.NotPorn &"
alias erotica="firefox -P 'erotica' %u &"
