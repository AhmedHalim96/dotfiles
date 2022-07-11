# Flex on the ubuntu users
#pfetch 

unsetopt completealiases

# Enable colors and change prompt:
autoload -U colors && colors
PS1="%B%{$fg[red]%}[%{$fg[yellow]%}%n%{$fg[green]%}@%{$fg[blue]%}%M %{$fg[magenta]%}%~%{$fg[red]%}]%{$reset_color%}$%b "

# History in cache directory:
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.cache/zshhistory
setopt appendhistory

#zsh completion from man page
#source $HOME/.zsh/zsh-completion-generator/zsh-completion-generator.plugin.zsh

# Basic auto/tab complete:
zstyle ':completion:*' menu select
zmodload zsh/complist
_comp_options+=(globdots)               # Include hidden files.

## completion stuff
zstyle ':compinstall' filename '$HOME/.zshrc'

fpath+=~/.config/zsh/zsh_functions

zcachedir="$HOME/.cache/zsh"
[[ -d "$zcachedir" ]] || mkdir -p "$zcachedir"

_update_zcomp() {
    setopt local_options
    setopt extendedglob
    autoload -Uz compinit
    local zcompf="$1/zcompdump"
    # use a separate file to determine when to regenerate, as compinit doesn't
    # always need to modify the compdump
    local zcompf_a="${zcompf}.augur"

    if [[ -e "$zcompf_a" && -f "$zcompf_a"(#qN.md-1) ]]; then
        compinit -C -d "$zcompf"
    else
        compinit -d "$zcompf"
        touch "$zcompf_a"
    fi
    # if zcompdump exists (and is non-zero), and is older than the .zwc file,
    # then regenerate
    if [[ -s "$zcompf" && (! -s "${zcompf}.zwc" || "$zcompf" -nt "${zcompf}.zwc") ]]; then
        # since file is mapped, it might be mapped right now (current shells), so
        # rename it then make a new one
        [[ -e "$zcompf.zwc" ]] && mv -f "$zcompf.zwc" "$zcompf.zwc.old"
        # compile it mapped, so multiple shells can share it (total mem reduction)
        # run in background
        zcompile -M "$zcompf" &!
    fi
}
_update_zcomp "$zcachedir"
unfunction _update_zcomp


# Custom ZSH Binds
bindkey '^ ' autosuggest-accept

#source ~/.config/zsh/.zprofile
source ~/.config/zsh/zshenv
source ~/.config/zsh/aliasrc
source ~/.config/zsh/zshvi
source ~/.config/zsh/zshplugins

# zoxide
#eval "$(zoxide init zsh)"

#the fuck
eval $(thefuck --alias) 
#use Beam instead of block
#echo -ne '\e[5 q' # Use beam shape cursor on startup.
#precmd () { print -Pn "\e]2;%n: %~\a" } # title bar prompt


###############################################
### Shell Prompts
###############################################

#Powerlevel10k
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
#source ~/.config/zsh/powerlevel10k/powerlevel10k.zsh-theme
#[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

#StarShip
eval "$(starship init zsh)"

# Set Spaceship ZSH as a prompt
#autoload -U promptinit; promptinit
#prompt spaceship

fpath=($fpath "/home/ahmed/.zfunctions")
