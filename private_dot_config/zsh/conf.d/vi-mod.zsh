# vi-mode aliases
zvm_vi_yank () {
	zvm_yank
	printf %s "${CUTBUFFER}" |  wl-copy -n
	zvm_exit_visual_mode
}

my_zvm_vi_delete() {
  zvm_vi_delete
  echo -en "${CUTBUFFER}" | wl-copy -n
}


my_zvm_vi_delete() {
  zvm_vi_delete
  echo -en "${CUTBUFFER}" | wl-copy -n
}

my_zvm_vi_change() {
  zvm_vi_change
  echo -en "${CUTBUFFER}" | wl-copy -n
}

my_zvm_vi_change_eol() {
  zvm_vi_change_eol
  echo -en "${CUTBUFFER}" | wl-copy -n
}

my_zvm_vi_put_after() {
  CUTBUFFER=$(wl-paste)
  zvm_vi_put_after
  zvm_highlight clear # zvm_vi_put_after introduces weird highlighting for me
}

my_zvm_vi_put_before() {
  CUTBUFFER=$(wl-paste)
  zvm_vi_put_before
  zvm_highlight clear # zvm_vi_put_before introduces weird highlighting for me
}

zvm_after_lazy_keybindings() {
  zvm_define_widget my_zvm_vi_yank
  zvm_define_widget my_zvm_vi_delete
  zvm_define_widget my_zvm_vi_change
  zvm_define_widget my_zvm_vi_change_eol
  zvm_define_widget my_zvm_vi_put_after
  zvm_define_widget my_zvm_vi_put_before

  
  zvm_bindkey vicmd 'dd' my_zvm_vi_delete

  zvm_bindkey visual 'x' my_zvm_vi_delete
  zvm_bindkey visual 'c' my_zvm_vi_change
  zvm_bindkey vicmd  'C' my_zvm_vi_change_eol
  zvm_bindkey vicmd  'p' my_zvm_vi_put_after
  zvm_bindkey vicmd  'P' my_zvm_vi_put_before
}
