# Add a `r` function to zsh that opens ranger either at the given directory or
# at the one autojump suggests
lf() {
  if [ "$1" != "" ]; then
    if [ -d "$1" ]; then
      ~/.local/bin/lfrun "$1"
    else
      ~/.local/bin/lfrun "$(autojump $1)"
    fi
  else
    ~/.local/bin/lfrun
  fi
	return $?
}
