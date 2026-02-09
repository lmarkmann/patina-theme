-- Patina Dark colorscheme for Neovim
-- Maintainer: markmann
-- License: MIT

vim.cmd('highlight clear')
if vim.fn.exists('syntax_on') then
  vim.cmd('syntax reset')
end

vim.o.background = 'dark'
vim.g.colors_name = 'patina-dark'

-- Color palette
local colors = {
  -- Background/UI
  bg = '#121212',
  fg = '#dbd7ca',
  line_highlight = '#1a1a1a',
  selection = '#42403d',
  line_number = '#333333',
  line_number_active = '#777777',
  border = '#2e2e2e',
  popup_bg = '#1a1a1a',
  statusline_fg = '#dbd7ca',
  statusline_bg = '#1a1a1a',
  statusline_inactive_fg = '#555555',
  statusline_inactive_bg = '#161616',

  -- Syntax
  comment = '#758575',
  keyword = '#4d9375',
  control = '#cb7676',
  operator = '#cb7676',
  string = '#c98a7d',
  number = '#4c9a91',
  func = '#80a665',
  variable = '#bd976a',
  parameter = '#b8a965',
  type = '#5da9a7',
  constant = '#c99076',
  boolean = '#c4a06a',
  punctuation = '#858585',
  import = '#758575',
  namespace = '#5da9a7',
  property = '#bd976a',
  macro = '#cb7676',
  escape = '#cb7676',

  -- Terminal ANSI
  black = '#2e2e2e',
  red = '#cb7676',
  green = '#4d9375',
  yellow = '#e6cc77',
  blue = '#6db3c2',
  magenta = '#c98a7d',
  cyan = '#5da9a7',
  white = '#dbd7ca',
  bright_black = '#585858',
  bright_red = '#cb7676',
  bright_green = '#4d9375',
  bright_yellow = '#e6cc77',
  bright_blue = '#6db3c2',
  bright_magenta = '#c98a7d',
  bright_cyan = '#5da9a7',
  bright_white = '#dbd7ca',

  -- Diff
  added = '#4d9375',
  deleted = '#cb7676',
  changed = '#bd976a',

  -- Diagnostics
  error = '#e05561',
  warning = '#e6cc77',
  info = '#6db3c2',
  hint = '#758575',
}

local function hl(group, opts)
  vim.api.nvim_set_hl(0, group, opts)
end

-- Editor highlights
hl('Normal', { fg = colors.fg, bg = colors.bg })
hl('NormalFloat', { fg = colors.fg, bg = colors.popup_bg })
hl('NormalNC', { fg = colors.fg, bg = colors.bg })
hl('Visual', { bg = colors.selection })
hl('CursorLine', { bg = colors.line_highlight })
hl('CursorColumn', { bg = colors.line_highlight })
hl('LineNr', { fg = colors.line_number })
hl('CursorLineNr', { fg = colors.line_number_active })
hl('SignColumn', { fg = colors.line_number, bg = colors.bg })
hl('StatusLine', { fg = colors.statusline_fg, bg = colors.statusline_bg })
hl('StatusLineNC', { fg = colors.statusline_inactive_fg, bg = colors.statusline_inactive_bg })
hl('Pmenu', { fg = colors.fg, bg = colors.popup_bg })
hl('PmenuSel', { fg = colors.fg, bg = colors.selection })
hl('PmenuSbar', { bg = colors.border })
hl('PmenuThumb', { bg = colors.line_number_active })
hl('TabLine', { fg = colors.statusline_inactive_fg, bg = colors.statusline_inactive_bg })
hl('TabLineFill', { bg = colors.statusline_inactive_bg })
hl('TabLineSel', { fg = colors.statusline_fg, bg = colors.statusline_bg })
hl('VertSplit', { fg = colors.border })
hl('WinSeparator', { fg = colors.border })
hl('Search', { fg = colors.bg, bg = colors.yellow })
hl('IncSearch', { fg = colors.bg, bg = colors.yellow })
hl('MatchParen', { fg = colors.yellow, bold = true })
hl('NonText', { fg = colors.line_number })
hl('SpecialKey', { fg = colors.line_number })
hl('Folded', { fg = colors.comment, bg = colors.line_highlight })
hl('FoldColumn', { fg = colors.line_number, bg = colors.bg })
hl('ColorColumn', { bg = colors.line_highlight })
hl('Conceal', { fg = colors.comment })
hl('Cursor', { fg = colors.bg, bg = colors.fg })
hl('lCursor', { fg = colors.bg, bg = colors.fg })
hl('CursorIM', { fg = colors.bg, bg = colors.fg })
hl('Directory', { fg = colors.blue })
hl('DiffAdd', { fg = colors.added, bg = colors.bg })
hl('DiffChange', { fg = colors.changed, bg = colors.bg })
hl('DiffDelete', { fg = colors.deleted, bg = colors.bg })
hl('DiffText', { fg = colors.changed, bg = colors.line_highlight })
hl('ErrorMsg', { fg = colors.error })
hl('WinBar', { fg = colors.fg })
hl('WinBarNC', { fg = colors.statusline_inactive_fg })
hl('ModeMsg', { fg = colors.fg })
hl('MoreMsg', { fg = colors.green })
hl('MsgArea', { fg = colors.fg })
hl('MsgSeparator', { fg = colors.border })
hl('Question', { fg = colors.blue })
hl('QuickFixLine', { bg = colors.selection })
hl('SpecialKey', { fg = colors.line_number })
hl('SpellBad', { undercurl = true, sp = colors.error })
hl('SpellCap', { undercurl = true, sp = colors.warning })
hl('SpellLocal', { undercurl = true, sp = colors.info })
hl('SpellRare', { undercurl = true, sp = colors.hint })
hl('Title', { fg = colors.blue, bold = true })
hl('WarningMsg', { fg = colors.warning })
hl('Whitespace', { fg = colors.line_number })
hl('WildMenu', { fg = colors.fg, bg = colors.selection })

-- Syntax highlighting
hl('Comment', { fg = colors.comment, italic = true })
hl('Constant', { fg = colors.constant })
hl('String', { fg = colors.string })
hl('Character', { fg = colors.string })
hl('Number', { fg = colors.number })
hl('Boolean', { fg = colors.boolean })
hl('Float', { fg = colors.number })
hl('Identifier', { fg = colors.variable })
hl('Function', { fg = colors.func })
hl('Statement', { fg = colors.keyword })
hl('Conditional', { fg = colors.control })
hl('Repeat', { fg = colors.control })
hl('Label', { fg = colors.keyword })
hl('Operator', { fg = colors.operator })
hl('Keyword', { fg = colors.keyword })
hl('Exception', { fg = colors.control })
hl('PreProc', { fg = colors.import })
hl('Include', { fg = colors.import })
hl('Define', { fg = colors.macro })
hl('Macro', { fg = colors.macro })
hl('Type', { fg = colors.type })
hl('StorageClass', { fg = colors.keyword })
hl('Structure', { fg = colors.type })
hl('Typedef', { fg = colors.type })
hl('Special', { fg = colors.escape })
hl('SpecialChar', { fg = colors.escape })
hl('Delimiter', { fg = colors.punctuation })
hl('Tag', { fg = colors.keyword })
hl('Error', { fg = colors.error })
hl('Todo', { fg = colors.yellow, bold = true })

-- Treesitter highlights
hl('@comment', { link = 'Comment' })
hl('@comment.documentation', { link = 'Comment' })
hl('@string', { link = 'String' })
hl('@string.escape', { fg = colors.escape })
hl('@string.regex', { fg = colors.escape })
hl('@string.special', { fg = colors.escape })
hl('@keyword', { fg = colors.keyword })
hl('@keyword.return', { fg = colors.control })
hl('@keyword.function', { fg = colors.keyword })
hl('@keyword.operator', { fg = colors.keyword })
hl('@keyword.import', { fg = colors.import })
hl('@keyword.conditional', { fg = colors.control })
hl('@keyword.repeat', { fg = colors.control })
hl('@keyword.exception', { fg = colors.control })
hl('@function', { fg = colors.func })
hl('@function.builtin', { fg = colors.func })
hl('@function.macro', { fg = colors.macro })
hl('@function.call', { fg = colors.func })
hl('@function.method', { fg = colors.func })
hl('@function.method.call', { fg = colors.func })
hl('@variable', { fg = colors.variable })
hl('@variable.parameter', { fg = colors.parameter })
hl('@variable.builtin', { fg = colors.variable })
hl('@variable.member', { fg = colors.property })
hl('@type', { fg = colors.type })
hl('@type.builtin', { fg = colors.type })
hl('@type.definition', { fg = colors.type })
hl('@type.qualifier', { fg = colors.keyword })
hl('@constant', { fg = colors.constant })
hl('@constant.builtin', { fg = colors.constant })
hl('@constant.macro', { fg = colors.constant })
hl('@number', { link = 'Number' })
hl('@number.float', { link = 'Float' })
hl('@boolean', { link = 'Boolean' })
hl('@operator', { fg = colors.operator })
hl('@punctuation', { fg = colors.punctuation })
hl('@punctuation.bracket', { fg = colors.punctuation })
hl('@punctuation.delimiter', { fg = colors.punctuation })
hl('@punctuation.special', { fg = colors.punctuation })
hl('@namespace', { fg = colors.namespace })
hl('@namespace.builtin', { fg = colors.namespace })
hl('@property', { fg = colors.property })
hl('@constructor', { fg = colors.type })
hl('@tag', { fg = colors.keyword })
hl('@tag.attribute', { fg = colors.property })
hl('@tag.delimiter', { fg = colors.punctuation })
hl('@attribute', { fg = colors.property })
hl('@attribute.builtin', { fg = colors.property })
hl('@label', { fg = colors.keyword })
hl('@module', { fg = colors.namespace })
hl('@character', { link = 'Character' })
hl('@character.special', { link = 'SpecialChar' })

-- LSP semantic tokens
hl('@lsp.type.namespace', { link = '@namespace' })
hl('@lsp.type.type', { link = '@type' })
hl('@lsp.type.class', { link = '@type' })
hl('@lsp.type.enum', { link = '@type' })
hl('@lsp.type.interface', { link = '@type' })
hl('@lsp.type.struct', { link = '@type' })
hl('@lsp.type.parameter', { link = '@variable.parameter' })
hl('@lsp.type.variable', { link = '@variable' })
hl('@lsp.type.property', { link = '@property' })
hl('@lsp.type.enumMember', { link = '@constant' })
hl('@lsp.type.function', { link = '@function' })
hl('@lsp.type.method', { link = '@function.method' })
hl('@lsp.type.macro', { link = '@macro' })
hl('@lsp.type.decorator', { link = '@attribute' })
hl('@lsp.type.comment', { link = '@comment' })

-- LSP diagnostics
hl('DiagnosticError', { fg = colors.error })
hl('DiagnosticWarn', { fg = colors.warning })
hl('DiagnosticInfo', { fg = colors.info })
hl('DiagnosticHint', { fg = colors.hint })
hl('DiagnosticOk', { fg = colors.green })

hl('DiagnosticVirtualTextError', { fg = colors.error, bg = colors.bg })
hl('DiagnosticVirtualTextWarn', { fg = colors.warning, bg = colors.bg })
hl('DiagnosticVirtualTextInfo', { fg = colors.info, bg = colors.bg })
hl('DiagnosticVirtualTextHint', { fg = colors.hint, bg = colors.bg })

hl('DiagnosticUnderlineError', { undercurl = true, sp = colors.error })
hl('DiagnosticUnderlineWarn', { undercurl = true, sp = colors.warning })
hl('DiagnosticUnderlineInfo', { undercurl = true, sp = colors.info })
hl('DiagnosticUnderlineHint', { undercurl = true, sp = colors.hint })

hl('DiagnosticSignError', { fg = colors.error, bg = colors.bg })
hl('DiagnosticSignWarn', { fg = colors.warning, bg = colors.bg })
hl('DiagnosticSignInfo', { fg = colors.info, bg = colors.bg })
hl('DiagnosticSignHint', { fg = colors.hint, bg = colors.bg })

hl('DiagnosticFloatingError', { fg = colors.error, bg = colors.popup_bg })
hl('DiagnosticFloatingWarn', { fg = colors.warning, bg = colors.popup_bg })
hl('DiagnosticFloatingInfo', { fg = colors.info, bg = colors.popup_bg })
hl('DiagnosticFloatingHint', { fg = colors.hint, bg = colors.popup_bg })

-- LSP references
hl('LspReferenceText', { bg = colors.selection })
hl('LspReferenceRead', { bg = colors.selection })
hl('LspReferenceWrite', { bg = colors.selection })

-- LSP signature help
hl('LspSignatureActiveParameter', { fg = colors.yellow, bold = true })

-- Git signs
hl('GitSignsAdd', { fg = colors.added, bg = colors.bg })
hl('GitSignsChange', { fg = colors.changed, bg = colors.bg })
hl('GitSignsDelete', { fg = colors.deleted, bg = colors.bg })

hl('GitSignsAddNr', { fg = colors.added, bg = colors.bg })
hl('GitSignsChangeNr', { fg = colors.changed, bg = colors.bg })
hl('GitSignsDeleteNr', { fg = colors.deleted, bg = colors.bg })

hl('GitSignsAddLn', { fg = colors.added, bg = colors.bg })
hl('GitSignsChangeLn', { fg = colors.changed, bg = colors.bg })
hl('GitSignsDeleteLn', { fg = colors.deleted, bg = colors.bg })

-- Git diff
hl('diffAdded', { fg = colors.added })
hl('diffRemoved', { fg = colors.deleted })
hl('diffChanged', { fg = colors.changed })
hl('diffOldFile', { fg = colors.deleted })
hl('diffNewFile', { fg = colors.added })
hl('diffFile', { fg = colors.blue })
hl('diffLine', { fg = colors.comment })
hl('diffIndexLine', { fg = colors.comment })

-- Terminal colors
vim.g.terminal_color_0 = colors.black
vim.g.terminal_color_1 = colors.red
vim.g.terminal_color_2 = colors.green
vim.g.terminal_color_3 = colors.yellow
vim.g.terminal_color_4 = colors.blue
vim.g.terminal_color_5 = colors.magenta
vim.g.terminal_color_6 = colors.cyan
vim.g.terminal_color_7 = colors.white
vim.g.terminal_color_8 = colors.bright_black
vim.g.terminal_color_9 = colors.bright_red
vim.g.terminal_color_10 = colors.bright_green
vim.g.terminal_color_11 = colors.bright_yellow
vim.g.terminal_color_12 = colors.bright_blue
vim.g.terminal_color_13 = colors.bright_magenta
vim.g.terminal_color_14 = colors.bright_cyan
vim.g.terminal_color_15 = colors.bright_white

-- Additional plugin support
-- Telescope
hl('TelescopeBorder', { fg = colors.border })
hl('TelescopePromptBorder', { fg = colors.border })
hl('TelescopeResultsBorder', { fg = colors.border })
hl('TelescopePreviewBorder', { fg = colors.border })
hl('TelescopeSelection', { bg = colors.selection })
hl('TelescopeSelectionCaret', { fg = colors.blue })
hl('TelescopeMatching', { fg = colors.yellow, bold = true })

-- nvim-cmp
hl('CmpItemAbbrMatch', { fg = colors.yellow, bold = true })
hl('CmpItemAbbrMatchFuzzy', { fg = colors.yellow })
hl('CmpItemKindVariable', { fg = colors.variable })
hl('CmpItemKindInterface', { fg = colors.type })
hl('CmpItemKindText', { fg = colors.fg })
hl('CmpItemKindFunction', { fg = colors.func })
hl('CmpItemKindMethod', { fg = colors.func })
hl('CmpItemKindKeyword', { fg = colors.keyword })
hl('CmpItemKindProperty', { fg = colors.property })
hl('CmpItemKindUnit', { fg = colors.type })

-- nvim-tree
hl('NvimTreeNormal', { fg = colors.fg, bg = colors.bg })
hl('NvimTreeRootFolder', { fg = colors.blue, bold = true })
hl('NvimTreeFolderName', { fg = colors.blue })
hl('NvimTreeFolderIcon', { fg = colors.blue })
hl('NvimTreeEmptyFolderName', { fg = colors.comment })
hl('NvimTreeOpenedFolderName', { fg = colors.blue })
hl('NvimTreeSymlink', { fg = colors.cyan })
hl('NvimTreeGitDirty', { fg = colors.changed })
hl('NvimTreeGitNew', { fg = colors.added })
hl('NvimTreeGitDeleted', { fg = colors.deleted })

-- Indent blankline
hl('IndentBlanklineChar', { fg = colors.border })
hl('IndentBlanklineContextChar', { fg = colors.line_number_active })

-- Which-key
hl('WhichKey', { fg = colors.blue })
hl('WhichKeyGroup', { fg = colors.keyword })
hl('WhichKeyDesc', { fg = colors.fg })
hl('WhichKeySeparator', { fg = colors.comment })
hl('WhichKeyFloat', { bg = colors.popup_bg })

-- Lazy.nvim
hl('LazyNormal', { fg = colors.fg, bg = colors.popup_bg })
hl('LazyButton', { bg = colors.selection })
hl('LazyButtonActive', { fg = colors.bg, bg = colors.blue })
hl('LazyH1', { fg = colors.bg, bg = colors.blue, bold = true })
hl('LazyH2', { fg = colors.blue, bold = true })
hl('LazyProgressDone', { fg = colors.green })
hl('LazyProgressTodo', { fg = colors.comment })
