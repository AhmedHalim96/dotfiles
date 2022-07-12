"##########################################
"#Settings
"##########################################
set encoding=utf-8
set number
syntax enable
set noswapfile
set scrolloff=7
set backspace=indent,eol,start
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
set smartindent
set smarttab
set autoindent
set fileformat=unix
set mouse=a
set nobackup
set nowritebackup
set updatetime=300
set timeoutlen=500
set formatoptions-=cro
set clipboard+=unnamedplus
set ignorecase
set smartcase
set cursorline
set linebreak
highlight CursorLine guibg=#2e323d guifg=fg
:au FocusLost * silent! wa
set cursorline
let mapleader = "\\"

"fixing the risizing problem
autocmd VimEnter * :silent exec "!kill -s SIGWINCH $PPID"

"##########################################
"#Plugins
"##########################################

call plug#begin()
  Plug 'preservim/nerdcommenter'
  Plug 'jiangmiao/auto-pairs'
  Plug 'norcalli/nvim-colorizer.lua'
  Plug 'vim-airline/vim-airline'
  Plug 'vim-airline/vim-airline-themes'
  Plug 'neoclide/coc.nvim', {'branch': 'release'}
  Plug 'scrooloose/nerdtree'
  Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
  Plug 'christoomey/vim-tmux-navigator'
  Plug 'aserebryakov/vim-todo-lists'
  Plug 'vimwiki/vimwiki'
  Plug 'godlygeek/tabular'
  Plug 'plasticboy/vim-markdown'
  Plug 'preservim/vim-lexical'
  Plug 'ptzz/lf.vim'
  Plug 'voldikss/vim-floaterm'
  Plug 'tpope/vim-surround'
call plug#end()

" Colorizer
if (has('termguicolors'))
    set termguicolors
endif


lua require 'colorizer'.setup()

" NERDCommenterToggle
nmap <C-_> <Plug>NERDCommenterToggle
imap <C-_> <Esc><Plug>NERDCommenterToggle i
vmap <C-_> <Plug>NERDCommenterToggle<CR>gv

" NERDTree
let NERDTreeQuitOnOpen=1
let g:NERDTreeMinimalUI=1
nmap <C-b> :NERDTreeToggle<CR>

" Tabs
let g:airline#extensions#tabline#enabled=1
let g:airline#extensions#tabline#fnamemode=':t'
nmap <leader>1 :bp<CR>
nmap <leader>2 :bn<CR>
nmap <C-w> :bd<CR>

" Todo
let g:VimTodoListsMoveItems = 0
let g:VimTodoListsDatesEnabled = 0

" vim wiki
let g:vimwiki_list = [{'path': '~/vimwiki/', 'syntax': 'markdown', 'ext': '.md'}]
let g:vimwiki_ext2syntax={".md": "markdown", '.markdown': 'markdown', '.mdown': 'markdown' }
let g:vimwiki_markdown_link_ext = 1
let g:taskwiki_markup_syntax = 'markdown'
let g:markdown_folding = 1

" lexical
let g:lexical#spell = 1 
let g:lexical#thesaurus = ['~/.config/nvim/words.txt',]
let g:lexical#spell_key = '<leader>s'
set nocompatible
filetype plugin on       " may already be in your .vimrc

augroup lexical
  autocmd!
  autocmd FileType markdown,mkd call lexical#init()
  autocmd FileType textile call lexical#init()
  autocmd FileType text call lexical#init({ 'spell': 0 })
augroup END


"##########################################
"# remaps
"##########################################

":map <S-s><S-s> :w<CR> 

" disable ex key
nnoremap Q <nop>

" Visual motion
nnoremap j gj
nnoremap gj j
nnoremap k gk
nnoremap gk k

" Moving lines
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

" tabs 
nnoremap zs :w\|bd<cr>
nnoremap zc :bd<cr>
nnoremap zn :bn<cr>
nnoremap zp :bp<cr>
