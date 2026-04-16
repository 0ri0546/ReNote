import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QAction, QToolBar, QDockWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QCheckBox, QColorDialog, QFontComboBox, QSpinBox,
    QStatusBar, QMessageBox, QSplitter, QFrame, QScrollArea,
    QGroupBox, QListWidget, QListWidgetItem, QMenu, QSizePolicy
)
from PyQt5.QtGui import (
    QFont, QTextCursor, QTextCharFormat, QColor, QPixmap,
    QTextBlockFormat, QTextListFormat, QKeySequence, QIcon,
    QPalette, QSyntaxHighlighter, QTextDocument
)
from PyQt5.QtCore import Qt, QRegExp, QTimer, pyqtSignal, QSize

# ──────────────────────────────────────────────────────────────────────────────
#  STYLE SHEET — Néo-futuriste bleu
# ──────────────────────────────────────────────────────────────────────────────
STYLESHEET = """
* {
    font-family: 'Segoe UI', 'Consolas', monospace;
    color: #c8e6ff;
}

QMainWindow {
    background-color: #060d1a;
}

/* ── Menus ── */
QMenuBar {
    background-color: #080f1e;
    border-bottom: 1px solid #003a6b;
    padding: 2px;
}
QMenuBar::item {
    padding: 5px 12px;
    background: transparent;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #003a6b;
    color: #00d4ff;
}
QMenu {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #003a6b;
    color: #00d4ff;
}

/* ── Toolbars ── */
QToolBar {
    background-color: #080f1e;
    border-bottom: 1px solid #003a6b;
    spacing: 3px;
    padding: 3px 6px;
}
QToolBar::separator {
    width: 1px;
    background-color: #003a6b;
    margin: 4px 6px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 3px 7px;
    min-width: 28px;
    font-size: 12px;
    color: #90caf9;
}
QToolButton:hover {
    background-color: #003a6b;
    border-color: #0077b6;
    color: #00d4ff;
}
QToolButton:pressed {
    background-color: #004f8a;
}
QToolButton:checked {
    background-color: #004f8a;
    border-color: #00d4ff;
    color: #00d4ff;
}

/* ── Editor ── */
QTextEdit {
    background-color: #050c18;
    color: #cce8ff;
    border: 1px solid #003a6b;
    selection-background-color: #004f8a;
    selection-color: #ffffff;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 8px;
}
QTextEdit:focus {
    border: 1px solid #0077b6;
}

/* ── Dock / panels ── */
QDockWidget {
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}
QDockWidget::title {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: bold;
    color: #00d4ff;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Inputs ── */
QLineEdit {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    border-radius: 4px;
    padding: 5px 8px;
    color: #c8e6ff;
}
QLineEdit:focus {
    border-color: #00d4ff;
}

QComboBox {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    border-radius: 4px;
    padding: 3px 8px;
    color: #c8e6ff;
    min-width: 60px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    selection-background-color: #003a6b;
    color: #c8e6ff;
}

QSpinBox {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    border-radius: 4px;
    padding: 3px 6px;
    color: #c8e6ff;
    min-width: 55px;
}
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #ffffff;
    border: none;
    width: 14px;
}

QFontComboBox {
    background-color: #0a1628;
    border: 1px solid #003a6b;
    border-radius: 4px;
    padding: 3px 8px;
    color: #c8e6ff;
    min-width: 130px;
}

/* ── Buttons ── */
QPushButton {
    background-color: #003a6b;
    border: 1px solid #0077b6;
    border-radius: 4px;
    padding: 5px 14px;
    color: #c8e6ff;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #004f8a;
    border-color: #00d4ff;
    color: #00d4ff;
}
QPushButton:pressed {
    background-color: #005fa3;
}
QPushButton#danger {
    background-color: #3a0000;
    border-color: #b00020;
    color: #ff6b6b;
}
QPushButton#danger:hover {
    background-color: #5a0000;
    border-color: #ff1744;
}
QPushButton#accent {
    background-color: #004f8a;
    border-color: #00d4ff;
    color: #00d4ff;
    font-weight: bold;
}
QPushButton#accent:hover {
    background-color: #006bb5;
}

/* ── Checkboxes ── */
QCheckBox {
    spacing: 6px;
    color: #90caf9;
    font-size: 12px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #003a6b;
    border-radius: 3px;
    background: #0a1628;
}
QCheckBox::indicator:checked {
    background-color: #004f8a;
    border-color: #00d4ff;
}

/* ── Labels ── */
QLabel {
    color: #90caf9;
    font-size: 12px;
}
QLabel#header {
    color: #00d4ff;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding-bottom: 3px;
}

/* ── Group boxes ── */
QGroupBox {
    border: 1px solid #003a6b;
    border-radius: 5px;
    margin-top: 10px;
    padding: 8px;
    font-size: 11px;
    color: #00d4ff;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 5px;
}

/* ── List widget (match results) ── */
QListWidget {
    background-color: #050c18;
    border: 1px solid #003a6b;
    border-radius: 4px;
    color: #90caf9;
    font-size: 12px;
    font-family: Consolas;
}
QListWidget::item:hover {
    background-color: #003a6b;
}
QListWidget::item:selected {
    background-color: #004f8a;
    color: #00d4ff;
}

/* ── Status bar ── */
QStatusBar {
    background-color: #080f1e;
    border-top: 1px solid #003a6b;
    color: #4a8fa8;
    font-size: 11px;
    padding: 2px 8px;
}

/* ── Scrollbars ── */
QScrollBar:vertical {
    background: #060d1a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #003a6b;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #0077b6;
}
QScrollBar:horizontal {
    background: #060d1a;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #003a6b;
    border-radius: 4px;
}
QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar::add-page, QScrollBar::sub-page {
    background: none; border: none;
}

/* ── Color picker buttons ── */
QPushButton.color-btn {
    min-width: 28px;
    max-width: 28px;
    min-height: 22px;
    max-height: 22px;
    border-radius: 3px;
    padding: 0;
}

/* ── Separators ── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #003a6b;
}
"""


# ──────────────────────────────────────────────────────────────────────────────
#  REGEX HIGHLIGHTER
# ──────────────────────────────────────────────────────────────────────────────
class RegexHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.pattern = None
        self.flags = 0
        self._highlight_format = QTextCharFormat()
        self._highlight_format.setBackground(QColor("#1a4f7a"))
        self._highlight_format.setForeground(QColor("#00d4ff"))

    def set_pattern(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags
        self.rehighlight()

    def highlightBlock(self, text):
        if not self.pattern:
            return
        try:
            for m in re.finditer(self.pattern, text, self.flags):
                self.setFormat(m.start(), m.end() - m.start(), self._highlight_format)
        except re.error:
            pass


# ──────────────────────────────────────────────────────────────────────────────
#  COLOR PICKER BUTTON
# ──────────────────────────────────────────────────────────────────────────────
class ColorButton(QPushButton):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, color=QColor("#00d4ff"), tooltip=""):
        super().__init__()
        self.setToolTip(tooltip)
        self.setFixedSize(26, 22)
        self.set_color(color)
        self.clicked.connect(self._pick)

    def set_color(self, color):
        self._color = color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                border: 1px solid #0077b6;
                border-radius: 3px;
            }}
            QPushButton:hover {{ border-color: #00d4ff; }}
        """)

    def _pick(self):
        c = QColorDialog.getColor(self._color, self, "Choisir une couleur")
        if c.isValid():
            self.set_color(c)
            self.colorChanged.emit(c)

    def color(self):
        return self._color


# ──────────────────────────────────────────────────────────────────────────────
#  WINDOW
# ──────────────────────────────────────────────────────────────────────────────
class ReNoteNeo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReNote ·  v1.0")
        self.setGeometry(60, 60, 1280, 800)
        self.setMinimumSize(900, 600)

        self._regex_timer = QTimer(self)
        self._regex_timer.setSingleShot(True)
        self._regex_timer.timeout.connect(self._on_regex_changed)

        self._setup_editor()
        self._setup_menus()
        self._setup_format_toolbar()
        self._setup_paragraph_toolbar()
        self._setup_regex_panel()
        self._setup_statusbar()

        self.editor.cursorPositionChanged.connect(self._update_status)
        self.editor.textChanged.connect(self._update_status)
        self.setStyleSheet(STYLESHEET)

    # ── EDITOR ────────────────────────────────────────────────────────────────
    def _setup_editor(self):
        self.editor = QTextEdit()
        self.editor.setAcceptDrops(True)
        self.editor.installEventFilter(self)
        self.editor.setTabStopWidth(40)
        font = QFont("Consolas", 13)
        self.editor.setFont(font)
        self.setCentralWidget(self.editor)
        self.highlighter = RegexHighlighter(self.editor.document())

    # ── MENUS ─────────────────────────────────────────────────────────────────
    def _setup_menus(self):
        mb = self.menuBar()

        # Fichier
        fm = mb.addMenu("&Fichier")
        self._add_action(fm, "Nouveau",        self.new_file,    "Ctrl+N")
        self._add_action(fm, "Ouvrir…",        self.load_file,   "Ctrl+O")
        self._add_action(fm, "Enregistrer…",   self.save_file,   "Ctrl+S")
        self._add_action(fm, "Enregistrer HTML…", self.save_html,"Ctrl+Shift+S")
        fm.addSeparator()
        self._add_action(fm, "Quitter",        self.close,       "Ctrl+Q")

        # Édition
        em = mb.addMenu("&Édition")
        self._add_action(em, "Annuler",   self.editor.undo,  "Ctrl+Z")
        self._add_action(em, "Rétablir",  self.editor.redo,  "Ctrl+Y")
        em.addSeparator()
        self._add_action(em, "Couper",    self.editor.cut,   "Ctrl+X")
        self._add_action(em, "Copier",    self.editor.copy,  "Ctrl+C")
        self._add_action(em, "Coller",    self.editor.paste, "Ctrl+V")
        em.addSeparator()
        self._add_action(em, "Tout sélectionner", self.editor.selectAll, "Ctrl+A")

        # Affichage
        vm = mb.addMenu("&Affichage")
        self._add_action(vm, "Panneau Regex", self._toggle_regex_dock, "Ctrl+R")

    def _add_action(self, menu, text, slot, shortcut=None):
        a = QAction(text, self)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        a.triggered.connect(slot)
        menu.addAction(a)
        return a

    # ── FORMAT TOOLBAR ────────────────────────────────────────────────────────
    def _setup_format_toolbar(self):
        tb = QToolBar("Format")
        tb.setIconSize(QSize(16, 16))
        tb.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(Qt.TopToolBarArea, tb)

        # Police
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Consolas"))
        self.font_combo.setToolTip("Police")
        self.font_combo.currentFontChanged.connect(self._change_font_family)
        tb.addWidget(self.font_combo)

        # Taille
        self.font_size = QSpinBox()
        self.font_size.setRange(6, 96)
        self.font_size.setValue(13)
        self.font_size.setToolTip("Taille")
        self.font_size.valueChanged.connect(self._change_font_size)
        tb.addWidget(self.font_size)

        tb.addSeparator()

        # Gras / Italique / Souligné / Barré
        self.act_bold = self._toolbar_action(tb, "G", self._toggle_bold,      "Gras (Ctrl+B)",          "Ctrl+B", checkable=True)
        self.act_italic = self._toolbar_action(tb, "I", self._toggle_italic,   "Italique (Ctrl+I)",      "Ctrl+I", checkable=True)
        self.act_under = self._toolbar_action(tb, "U̲", self._toggle_underline, "Souligné (Ctrl+U)",     "Ctrl+U", checkable=True)
        self.act_strike = self._toolbar_action(tb, "S̶", self._toggle_strike,   "Barré (Ctrl+Shift+X)",  "Ctrl+Shift+X", checkable=True)
        self.act_super  = self._toolbar_action(tb, "x²", self._toggle_super,   "Exposant",               None, checkable=True)
        self.act_sub    = self._toolbar_action(tb, "x₂", self._toggle_sub,     "Indice",                 None, checkable=True)

        tb.addSeparator()

        # Couleurs
        lbl_fg = QLabel(" A ")
        lbl_fg.setToolTip("Couleur du texte")
        tb.addWidget(lbl_fg)
        self.color_fg = ColorButton(QColor("#cce8ff"), "Couleur du texte")
        self.color_fg.colorChanged.connect(self._change_color_fg)
        tb.addWidget(self.color_fg)

        lbl_bg = QLabel(" ◧ ")
        lbl_bg.setToolTip("Surlignage")
        tb.addWidget(lbl_bg)
        self.color_bg = ColorButton(QColor("#003a6b"), "Couleur de surlignage")
        self.color_bg.colorChanged.connect(self._change_color_bg)
        tb.addWidget(self.color_bg)

        tb.addSeparator()

        # Effacer formatage
        self._toolbar_action(tb, "⌫ Format", self._clear_format, "Effacer le formatage")

        self.editor.cursorPositionChanged.connect(self._sync_format_toolbar)

    def _toolbar_action(self, tb, text, slot, tooltip="", shortcut=None, checkable=False):
        a = QAction(text, self)
        a.setToolTip(tooltip)
        a.setCheckable(checkable)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        a.triggered.connect(slot)
        tb.addAction(a)
        return a

    # ── PARAGRAPH TOOLBAR ─────────────────────────────────────────────────────
    def _setup_paragraph_toolbar(self):
        tb = QToolBar("Paragraphe")
        tb.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(Qt.TopToolBarArea, tb)

        # Alignements
        self.act_left   = self._toolbar_action(tb, "⬛L", lambda: self._align(Qt.AlignLeft),    "Aligner à gauche",  "Ctrl+L", checkable=True)
        self.act_center = self._toolbar_action(tb, "⬛C", lambda: self._align(Qt.AlignHCenter), "Centrer",           "Ctrl+E", checkable=True)
        self.act_right  = self._toolbar_action(tb, "⬛R", lambda: self._align(Qt.AlignRight),   "Aligner à droite",  "Ctrl+Shift+R", checkable=True)
        self.act_justify= self._toolbar_action(tb, "⬛J", lambda: self._align(Qt.AlignJustify),"Justifier",          "Ctrl+J", checkable=True)
        self.act_left.setChecked(True)

        tb.addSeparator()

        # Listes
        self._toolbar_action(tb, "• Liste",  self._list_bullet,  "Liste à puces")
        self._toolbar_action(tb, "1. Liste", self._list_ordered, "Liste numérotée")

        tb.addSeparator()

        # Indentation
        self._toolbar_action(tb, "→ Indent",  self.indent_more,  "Augmenter l'indentation", "Tab")
        self._toolbar_action(tb, "← Indent",  self.indent_less,  "Réduire l'indentation",   "Shift+Tab")

        tb.addSeparator()

        # Interligne
        lbl = QLabel("  Ligne:")
        tb.addWidget(lbl)
        self.line_spacing = QComboBox()
        self.line_spacing.addItems(["Simple", "1.15", "1.5", "Double"])
        self.line_spacing.setToolTip("Interligne")
        self.line_spacing.currentIndexChanged.connect(self._change_line_spacing)
        tb.addWidget(self.line_spacing)

        tb.addSeparator()

        # Insérer image
        self._toolbar_action(tb, "🖼 Image", self._insert_image, "Insérer une image")

    # ── REGEX DOCK ────────────────────────────────────────────────────────────
    def _setup_regex_panel(self):
        self.regex_dock = QDockWidget("Moteur Regex", self)
        self.regex_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.regex_dock)

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setSpacing(10)
        lay.setContentsMargins(10, 10, 10, 10)

        # ── Pattern ──
        grp_search = QGroupBox("Recherche")
        gl = QVBoxLayout(grp_search)

        self.regex_input = QLineEdit()
        self.regex_input.setPlaceholderText("Pattern regex... ex : \*\*(.*?)\*\* ")
        self.regex_input.textChanged.connect(self._schedule_regex)
        gl.addWidget(self.regex_input)

        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Remplacement... ex : \\1, \\2 ")
        gl.addWidget(self.replace_input)

        # Flags
        flag_row = QHBoxLayout()
        self.chk_ignorecase = QCheckBox("Ignorer casse")
        self.chk_multiline  = QCheckBox("Multiligne")
        self.chk_dotall     = QCheckBox(". = tout")
        for c in (self.chk_ignorecase, self.chk_multiline, self.chk_dotall):
            c.stateChanged.connect(self._schedule_regex)
            flag_row.addWidget(c)
        gl.addLayout(flag_row)

        lay.addWidget(grp_search)

        # ── Boutons ──
        btn_row = QHBoxLayout()
        self.btn_prev = QPushButton("◀ Préc.")
        self.btn_prev.setToolTip("Match précédent")
        self.btn_prev.clicked.connect(self._prev_match)
        btn_row.addWidget(self.btn_prev)

        self.btn_next = QPushButton("Suiv. ▶")
        self.btn_next.setToolTip("Match suivant")
        self.btn_next.clicked.connect(self._next_match)
        btn_row.addWidget(self.btn_next)

        lay.addLayout(btn_row)

        btn_row2 = QHBoxLayout()
        self.btn_replace_one = QPushButton("Remplacer")
        self.btn_replace_one.setToolTip("Remplacer le match courant")
        self.btn_replace_one.clicked.connect(self._replace_current)
        btn_row2.addWidget(self.btn_replace_one)

        self.btn_replace_all = QPushButton("Tout remplacer")
        self.btn_replace_all.setObjectName("accent")
        self.btn_replace_all.clicked.connect(self._replace_all)
        btn_row2.addWidget(self.btn_replace_all)

        lay.addLayout(btn_row2)

        self.btn_clear = QPushButton("✕ Effacer highlights")
        self.btn_clear.setObjectName("danger")
        self.btn_clear.clicked.connect(self._clear_regex)
        lay.addWidget(self.btn_clear)

        # ── Résultats ──
        grp_res = QGroupBox("Correspondances")
        rl = QVBoxLayout(grp_res)

        self.match_list = QListWidget()
        self.match_list.setToolTip("Cliquer pour naviguer vers le match")
        self.match_list.itemClicked.connect(self._jump_to_match)
        rl.addWidget(self.match_list)

        self.lbl_count = QLabel("0 correspondance(s)")
        self.lbl_count.setAlignment(Qt.AlignCenter)
        rl.addWidget(self.lbl_count)

        lay.addWidget(grp_res)

        lay.addStretch()
        self.regex_dock.setWidget(container)

        self._matches = []
        self._current_match = -1

    def _toggle_regex_dock(self):
        self.regex_dock.setVisible(not self.regex_dock.isVisible())

    # ── STATUS BAR ────────────────────────────────────────────────────────────
    def _setup_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.lbl_pos = QLabel("Ligne 1 · Col 1")
        self.lbl_words = QLabel("0 mots")
        self.lbl_chars = QLabel("0 caractères")
        for w in (self.lbl_pos, self.lbl_words, self.lbl_chars):
            self.status.addPermanentWidget(w)

    def _update_status(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col  = cursor.columnNumber() + 1
        text = self.editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        self.lbl_pos.setText(f"Ligne {line} · Col {col}")
        self.lbl_words.setText(f"{words} mots")
        self.lbl_chars.setText(f"{len(text)} caractères")

    # ── FORMAT ACTIONS ────────────────────────────────────────────────────────
    def _current_fmt(self):
        return self.editor.textCursor().charFormat()

    def _apply_fmt(self, fmt):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

    def _toggle_bold(self):
        fmt = QTextCharFormat()
        w = QFont.Normal if self._current_fmt().fontWeight() == QFont.Bold else QFont.Bold
        fmt.setFontWeight(w)
        self._apply_fmt(fmt)

    def _toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self._current_fmt().fontItalic())
        self._apply_fmt(fmt)

    def _toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self._current_fmt().fontUnderline())
        self._apply_fmt(fmt)

    def _toggle_strike(self):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(not self._current_fmt().fontStrikeOut())
        self._apply_fmt(fmt)

    def _toggle_super(self):
        fmt = QTextCharFormat()
        va = self._current_fmt().verticalAlignment()
        new_va = QTextCharFormat.AlignNormal if va == QTextCharFormat.AlignSuperScript else QTextCharFormat.AlignSuperScript
        fmt.setVerticalAlignment(new_va)
        self._apply_fmt(fmt)

    def _toggle_sub(self):
        fmt = QTextCharFormat()
        va = self._current_fmt().verticalAlignment()
        new_va = QTextCharFormat.AlignNormal if va == QTextCharFormat.AlignSubScript else QTextCharFormat.AlignSubScript
        fmt.setVerticalAlignment(new_va)
        self._apply_fmt(fmt)

    def _change_font_family(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self._apply_fmt(fmt)

    def _change_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._apply_fmt(fmt)

    def _change_color_fg(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self._apply_fmt(fmt)

    def _change_color_bg(self, color):
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        self._apply_fmt(fmt)

    def _clear_format(self):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.BlockUnderCursor)
        cursor.setCharFormat(QTextCharFormat())
        fmt = QTextBlockFormat()
        cursor.setBlockFormat(fmt)

    def _sync_format_toolbar(self):
        fmt = self._current_fmt()
        self.act_bold.setChecked(fmt.fontWeight() == QFont.Bold)
        self.act_italic.setChecked(fmt.fontItalic())
        self.act_under.setChecked(fmt.fontUnderline())
        self.act_strike.setChecked(fmt.fontStrikeOut())
        self.act_super.setChecked(fmt.verticalAlignment() == QTextCharFormat.AlignSuperScript)
        self.act_sub.setChecked(fmt.verticalAlignment() == QTextCharFormat.AlignSubScript)
        if fmt.fontPointSize() > 0:
            self.font_size.blockSignals(True)
            self.font_size.setValue(int(fmt.fontPointSize()))
            self.font_size.blockSignals(False)

    # ── PARAGRAPH ACTIONS ─────────────────────────────────────────────────────
    def _align(self, alignment):
        self.editor.setAlignment(alignment)
        for act, aln in ((self.act_left, Qt.AlignLeft), (self.act_center, Qt.AlignHCenter),
                         (self.act_right, Qt.AlignRight), (self.act_justify, Qt.AlignJustify)):
            act.setChecked(alignment == aln)

    def _list_bullet(self):
        cursor = self.editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDisc)
        cursor.createList(fmt)

    def _list_ordered(self):
        cursor = self.editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDecimal)
        cursor.createList(fmt)

    def indent_more(self):
        cursor = self.editor.textCursor()
        if cursor.currentList():
            fmt = cursor.currentList().format()
            fmt.setIndent(fmt.indent() + 1)
            cursor.currentList().setFormat(fmt)
        else:
            blk = cursor.blockFormat()
            blk.setLeftMargin(blk.leftMargin() + 20)
            cursor.setBlockFormat(blk)

    def indent_less(self):
        cursor = self.editor.textCursor()
        if cursor.currentList():
            fmt = cursor.currentList().format()
            fmt.setIndent(max(1, fmt.indent() - 1))
            cursor.currentList().setFormat(fmt)
        else:
            blk = cursor.blockFormat()
            blk.setLeftMargin(max(0, blk.leftMargin() - 20))
            cursor.setBlockFormat(blk)

    def _change_line_spacing(self, idx):
        ratios = {0: 100, 1: 115, 2: 150, 3: 200}
        blk = QTextBlockFormat()
        blk.setLineHeight(ratios[idx], QTextBlockFormat.ProportionalHeight)
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(blk)

    # ── IMAGE ─────────────────────────────────────────────────────────────────
    def _insert_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Insérer une image", "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"
        )
        if path:
            cursor = self.editor.textCursor()
            cursor.insertImage(path)

    # ── FILE ─────────────────────────────────────────────────────────────────
    def new_file(self):
        if self.editor.document().isModified():
            r = QMessageBox.question(self, "Nouveau", "Sauvegarder avant de créer un nouveau fichier ?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if r == QMessageBox.Yes:
                self.save_file()
            elif r == QMessageBox.Cancel:
                return
        self.editor.clear()
        self.editor.document().setModified(False)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer", "", "Texte brut (*.txt);;HTML (*.html)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                if path.endswith(".html"):
                    f.write(self.editor.toHtml())
                else:
                    f.write(self.editor.toPlainText())

    def save_html(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer en HTML", "", "HTML (*.html)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toHtml())

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir", "",
            "Tous fichiers (*.txt *.html *.htm *.md);;Texte (*.txt);;HTML (*.html *.htm)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if path.endswith((".html", ".htm")):
                self.editor.setHtml(content)
            else:
                self.editor.setPlainText(content)
            self.editor.document().setModified(False)

    # ── REGEX ENGINE ─────────────────────────────────────────────────────────
    def _build_flags(self):
        flags = 0
        if self.chk_ignorecase.isChecked(): flags |= re.IGNORECASE
        if self.chk_multiline.isChecked():  flags |= re.MULTILINE
        if self.chk_dotall.isChecked():     flags |= re.DOTALL
        return flags

    def _schedule_regex(self):
        self._regex_timer.start(300)

    def _on_regex_changed(self):
        pattern = self.regex_input.text()
        self.match_list.clear()
        self._matches = []
        self._current_match = -1

        if not pattern:
            self.highlighter.set_pattern(None)
            self.lbl_count.setText("0 correspondance(s)")
            return

        flags = self._build_flags()
        try:
            text = self.editor.toPlainText()
            self._matches = list(re.finditer(pattern, text, flags))
            self.highlighter.set_pattern(pattern, flags)
            self.lbl_count.setText(f"{len(self._matches)} correspondance(s)")
            for i, m in enumerate(self._matches):
                line_no = text[:m.start()].count('\n') + 1
                item = QListWidgetItem(f"#{i+1}  L.{line_no}  «{m.group()[:40]}»")
                item.setData(Qt.UserRole, m.start())
                self.match_list.addItem(item)
            if self._matches:
                self._current_match = 0
                self._jump_to_pos(self._matches[0].start(), self._matches[0].end())
        except re.error as e:
            self.lbl_count.setText(f"⚠ Erreur : {e}")

    def _jump_to_pos(self, start, end):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()

    def _jump_to_match(self, item):
        pos = item.data(Qt.UserRole)
        idx = self.match_list.row(item)
        self._current_match = idx
        m = self._matches[idx]
        self._jump_to_pos(m.start(), m.end())

    def _next_match(self):
        if not self._matches: return
        self._current_match = (self._current_match + 1) % len(self._matches)
        m = self._matches[self._current_match]
        self._jump_to_pos(m.start(), m.end())
        self.match_list.setCurrentRow(self._current_match)

    def _prev_match(self):
        if not self._matches: return
        self._current_match = (self._current_match - 1) % len(self._matches)
        m = self._matches[self._current_match]
        self._jump_to_pos(m.start(), m.end())
        self.match_list.setCurrentRow(self._current_match)

    def _replace_current(self):
        if not self._matches or self._current_match < 0: return
        pattern = self.regex_input.text()
        replace = self.replace_input.text()
        flags   = self._build_flags()
        text    = self.editor.toPlainText()
        m = self._matches[self._current_match]
        try:
            new_piece = re.sub(pattern, replace, m.group(), count=1, flags=flags)
            new_text  = text[:m.start()] + new_piece + text[m.end():]
            self.editor.setPlainText(new_text)
            self._on_regex_changed()
        except re.error as e:
            QMessageBox.warning(self, "Regex", f"Erreur : {e}")

    def _replace_all(self):
        pattern = self.regex_input.text()
        replace = self.replace_input.text()
        if not pattern: return
        flags = self._build_flags()
        text  = self.editor.toPlainText()
        try:
            new_text, n = re.subn(pattern, replace, text, flags=flags)
            self.editor.setPlainText(new_text)
            self._on_regex_changed()
            self.status.showMessage(f"✔ {n} remplacement(s) effectué(s)", 4000)
        except re.error as e:
            QMessageBox.warning(self, "Regex", f"Erreur : {e}")

    def _clear_regex(self):
        self.regex_input.clear()
        self.replace_input.clear()
        self.highlighter.set_pattern(None)
        self.match_list.clear()
        self.lbl_count.setText("0 correspondance(s)")
        self._matches = []
        self._current_match = -1

    # ── DRAG & DROP ───────────────────────────────────────────────────────────
    def eventFilter(self, source, event):
        if event.type() == event.Drop and source is self.editor:
            if event.mimeData().hasImage():
                cursor = self.editor.textCursor()
                cursor.insertImage(event.mimeData().imageData())
                return True
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    local = url.toLocalFile()
                    if local.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                        self.editor.textCursor().insertImage(local)
                return True
        return super().eventFilter(source, event)

    # ── CLOSE ─────────────────────────────────────────────────────────────────
    def closeEvent(self, event):
        if self.editor.document().isModified():
            r = QMessageBox.question(self, "Quitter", "Sauvegarder avant de quitter ?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if r == QMessageBox.Yes:
                self.save_file()
            elif r == QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ReNoteNeo()
    window.show()
    sys.exit(app.exec_())
