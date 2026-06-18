from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenuBar,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 920)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setContentsMargins(24, 20, 24, 20)
        self.rootLayout.setSpacing(18)

        self._build_header()
        self._build_workspace()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def _build_header(self):
        self.headerCard = QFrame(self.centralwidget)
        self.headerCard.setObjectName("HeaderCard")
        header_layout = QHBoxLayout(self.headerCard)
        header_layout.setContentsMargins(28, 24, 28, 24)
        header_layout.setSpacing(20)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(6)

        self.lblEyebrow = QLabel(self.headerCard)
        self.lblEyebrow.setObjectName("lblEyebrow")
        title_layout.addWidget(self.lblEyebrow)

        self.lblHeroTitle = QLabel(self.headerCard)
        self.lblHeroTitle.setObjectName("lblHeroTitle")
        self.lblHeroTitle.setWordWrap(True)
        title_layout.addWidget(self.lblHeroTitle)

        self.lblHeroSubtitle = QLabel(self.headerCard)
        self.lblHeroSubtitle.setObjectName("lblHeroSubtitle")
        self.lblHeroSubtitle.setWordWrap(True)
        title_layout.addWidget(self.lblHeroSubtitle)
        title_layout.addStretch()

        header_layout.addLayout(title_layout, 1)

        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(10)

        self.summaryCard = QFrame(self.headerCard)
        self.summaryCard.setObjectName("SummaryCard")
        summary_grid = QGridLayout(self.summaryCard)
        summary_grid.setContentsMargins(18, 16, 18, 16)
        summary_grid.setHorizontalSpacing(18)
        summary_grid.setVerticalSpacing(10)

        self.lblSummaryExcelLabel = QLabel(self.summaryCard)
        self.lblSummaryExcelLabel.setObjectName("MetricLabel")
        summary_grid.addWidget(self.lblSummaryExcelLabel, 0, 0)

        self.lblSummaryExcelValue = QLabel(self.summaryCard)
        self.lblSummaryExcelValue.setObjectName("MetricValue")
        summary_grid.addWidget(self.lblSummaryExcelValue, 1, 0)

        self.lblSummaryRecipientsLabel = QLabel(self.summaryCard)
        self.lblSummaryRecipientsLabel.setObjectName("MetricLabel")
        summary_grid.addWidget(self.lblSummaryRecipientsLabel, 0, 1)

        self.lblSummaryRecipientsValue = QLabel(self.summaryCard)
        self.lblSummaryRecipientsValue.setObjectName("MetricValue")
        summary_grid.addWidget(self.lblSummaryRecipientsValue, 1, 1)

        self.lblSummaryAttachmentsLabel = QLabel(self.summaryCard)
        self.lblSummaryAttachmentsLabel.setObjectName("MetricLabel")
        summary_grid.addWidget(self.lblSummaryAttachmentsLabel, 0, 2)

        self.lblSummaryAttachmentsValue = QLabel(self.summaryCard)
        self.lblSummaryAttachmentsValue.setObjectName("MetricValue")
        summary_grid.addWidget(self.lblSummaryAttachmentsValue, 1, 2)

        summary_layout.addWidget(self.summaryCard)
        header_layout.addLayout(summary_layout)

        self.rootLayout.addWidget(self.headerCard)

    def _build_workspace(self):
        self.workspaceSplitter = QSplitter(Qt.Horizontal, self.centralwidget)
        self.workspaceSplitter.setObjectName("workspaceSplitter")
        self.workspaceSplitter.setChildrenCollapsible(False)

        self._build_left_sidebar()
        self._build_compose_center()
        self._build_right_sidebar()

        self.workspaceSplitter.addWidget(self.leftSidebar)
        self.workspaceSplitter.addWidget(self.composePanel)
        self.workspaceSplitter.addWidget(self.rightSidebar)
        self.workspaceSplitter.setStretchFactor(0, 0)
        self.workspaceSplitter.setStretchFactor(1, 1)
        self.workspaceSplitter.setStretchFactor(2, 0)
        self.workspaceSplitter.setSizes([300, 760, 320])

        self.rootLayout.addWidget(self.workspaceSplitter, 1)

    def _build_left_sidebar(self):
        self.leftSidebar = QFrame(self.centralwidget)
        self.leftSidebar.setObjectName("SidebarCard")
        self.leftSidebar.setMinimumWidth(280)
        left_layout = QVBoxLayout(self.leftSidebar)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(16)

        self.lblSetupTitle = QLabel(self.leftSidebar)
        self.lblSetupTitle.setObjectName("PanelTitle")
        left_layout.addWidget(self.lblSetupTitle)

        self.dataCard = QFrame(self.leftSidebar)
        self.dataCard.setObjectName("PanelSection")
        data_layout = QVBoxLayout(self.dataCard)
        data_layout.setContentsMargins(16, 16, 16, 16)
        data_layout.setSpacing(12)

        self.lblDataTitle = QLabel(self.dataCard)
        self.lblDataTitle.setObjectName("SectionTitle")
        data_layout.addWidget(self.lblDataTitle)

        self.lblExcel = QLabel(self.dataCard)
        self.lblExcel.setObjectName("FieldLabel")
        data_layout.addWidget(self.lblExcel)

        excel_row = QHBoxLayout()
        excel_row.setSpacing(8)
        self.txtExcel = QLineEdit(self.dataCard)
        self.txtExcel.setObjectName("txtExcel")
        self.txtExcel.setReadOnly(True)
        excel_row.addWidget(self.txtExcel, 1)

        self.btnBrowseExcel = QPushButton(self.dataCard)
        self.btnBrowseExcel.setObjectName("btnBrowseExcel")
        excel_row.addWidget(self.btnBrowseExcel)
        data_layout.addLayout(excel_row)

        self.lblEmailCol = QLabel(self.dataCard)
        self.lblEmailCol.setObjectName("FieldLabel")
        data_layout.addWidget(self.lblEmailCol)

        self.comboEmailCol = QComboBox(self.dataCard)
        self.comboEmailCol.setObjectName("comboEmailCol")
        data_layout.addWidget(self.comboEmailCol)

        self.lblMailProvider = QLabel(self.dataCard)
        self.lblMailProvider.setObjectName("FieldLabel")
        data_layout.addWidget(self.lblMailProvider)

        self.comboMailProvider = QComboBox(self.dataCard)
        self.comboMailProvider.setObjectName("comboMailProvider")
        data_layout.addWidget(self.comboMailProvider)

        self.lblGmailUser = QLabel(self.dataCard)
        self.lblGmailUser.setObjectName("FieldLabel")
        data_layout.addWidget(self.lblGmailUser)

        self.txtGmailUser = QLineEdit(self.dataCard)
        self.txtGmailUser.setObjectName("txtGmailUser")
        data_layout.addWidget(self.txtGmailUser)

        self.lblGmailPassword = QLabel(self.dataCard)
        self.lblGmailPassword.setObjectName("FieldLabel")
        data_layout.addWidget(self.lblGmailPassword)

        self.txtGmailPassword = QLineEdit(self.dataCard)
        self.txtGmailPassword.setObjectName("txtGmailPassword")
        self.txtGmailPassword.setEchoMode(QLineEdit.EchoMode.Password)
        data_layout.addWidget(self.txtGmailPassword)

        self.lblGmailHint = QLabel(self.dataCard)
        self.lblGmailHint.setObjectName("HelperLabel")
        self.lblGmailHint.setWordWrap(True)
        data_layout.addWidget(self.lblGmailHint)

        left_layout.addWidget(self.dataCard)

        self.grpPlaceholders = QGroupBox(self.leftSidebar)
        self.grpPlaceholders.setObjectName("grpPlaceholders")
        placeholders_layout = QVBoxLayout(self.grpPlaceholders)
        placeholders_layout.setContentsMargins(16, 18, 16, 16)
        placeholders_layout.setSpacing(10)

        self.lblPhHint = QLabel(self.grpPlaceholders)
        self.lblPhHint.setObjectName("HelperLabel")
        self.lblPhHint.setWordWrap(True)
        placeholders_layout.addWidget(self.lblPhHint)

        self.listPlaceholders = QListWidget(self.grpPlaceholders)
        self.listPlaceholders.setObjectName("listPlaceholders")
        self.listPlaceholders.setSelectionMode(QAbstractItemView.ExtendedSelection)
        placeholders_layout.addWidget(self.listPlaceholders, 1)
        left_layout.addWidget(self.grpPlaceholders, 1)

    def _build_compose_center(self):
        self.composePanel = QFrame(self.centralwidget)
        self.composePanel.setObjectName("ComposePanel")
        self.composePanel.setMinimumWidth(560)
        compose_layout = QVBoxLayout(self.composePanel)
        compose_layout.setContentsMargins(0, 0, 0, 0)
        compose_layout.setSpacing(16)

        self.composeCard = QFrame(self.composePanel)
        self.composeCard.setObjectName("ComposeCard")
        compose_card_layout = QVBoxLayout(self.composeCard)
        compose_card_layout.setContentsMargins(24, 22, 24, 22)
        compose_card_layout.setSpacing(16)

        compose_header = QHBoxLayout()
        compose_header.setSpacing(12)

        compose_title_layout = QVBoxLayout()
        compose_title_layout.setSpacing(4)

        self.lblComposeTitle = QLabel(self.composeCard)
        self.lblComposeTitle.setObjectName("PanelTitle")
        compose_title_layout.addWidget(self.lblComposeTitle)

        self.lblComposeSubtitle = QLabel(self.composeCard)
        self.lblComposeSubtitle.setObjectName("HelperLabel")
        self.lblComposeSubtitle.setWordWrap(True)
        compose_title_layout.addWidget(self.lblComposeSubtitle)
        compose_header.addLayout(compose_title_layout, 1)

        self.modeCard = QFrame(self.composeCard)
        self.modeCard.setObjectName("ModeCard")
        mode_layout = QHBoxLayout(self.modeCard)
        mode_layout.setContentsMargins(14, 12, 14, 12)
        mode_layout.setSpacing(14)

        self.radioDraft = QRadioButton(self.modeCard)
        self.radioDraft.setObjectName("radioDraft")
        mode_layout.addWidget(self.radioDraft)

        self.radioSend = QRadioButton(self.modeCard)
        self.radioSend.setObjectName("radioSend")
        self.radioSend.setChecked(True)
        mode_layout.addWidget(self.radioSend)
        compose_header.addWidget(self.modeCard)

        compose_card_layout.addLayout(compose_header)

        self.txtSubject = QLineEdit(self.composeCard)
        self.txtSubject.setObjectName("txtSubject")
        compose_card_layout.addWidget(self.txtSubject)

        self.editorCard = QFrame(self.composeCard)
        self.editorCard.setObjectName("EditorCard")
        editor_layout = QVBoxLayout(self.editorCard)
        editor_layout.setContentsMargins(12, 12, 12, 12)
        editor_layout.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.btnBold = QPushButton(self.editorCard)
        self.btnBold.setObjectName("btnBold")
        self.btnBold.setCheckable(True)
        toolbar.addWidget(self.btnBold)

        self.btnItalic = QPushButton(self.editorCard)
        self.btnItalic.setObjectName("btnItalic")
        self.btnItalic.setCheckable(True)
        toolbar.addWidget(self.btnItalic)

        self.btnUnderline = QPushButton(self.editorCard)
        self.btnUnderline.setObjectName("btnUnderline")
        self.btnUnderline.setCheckable(True)
        toolbar.addWidget(self.btnUnderline)

        toolbar.addStretch()
        editor_layout.addLayout(toolbar)

        self.lblBody = QTextEdit(self.editorCard)
        self.lblBody.setObjectName("lblBody")
        editor_layout.addWidget(self.lblBody, 1)
        compose_card_layout.addWidget(self.editorCard, 1)

        actions_row = QHBoxLayout()
        actions_row.setSpacing(10)

        self.btnValidate = QPushButton(self.composeCard)
        self.btnValidate.setObjectName("btnValidate")
        actions_row.addWidget(self.btnValidate)

        self.btnPreview = QPushButton(self.composeCard)
        self.btnPreview.setObjectName("btnPreview")
        actions_row.addWidget(self.btnPreview)

        self.btnCheck = QPushButton(self.composeCard)
        self.btnCheck.setObjectName("btnCheck")
        actions_row.addWidget(self.btnCheck)

        actions_row.addStretch()

        self.btnRun = QPushButton(self.composeCard)
        self.btnRun.setObjectName("btnRun")
        self.btnRun.setProperty("variant", "primary")
        actions_row.addWidget(self.btnRun)

        compose_card_layout.addLayout(actions_row)
        compose_layout.addWidget(self.composeCard, 1)

    def _build_right_sidebar(self):
        self.rightSidebar = QFrame(self.centralwidget)
        self.rightSidebar.setObjectName("SidebarCard")
        self.rightSidebar.setMinimumWidth(320)
        right_layout = QVBoxLayout(self.rightSidebar)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(16)

        self.grpPersonalPdf = QGroupBox(self.rightSidebar)
        self.grpPersonalPdf.setObjectName("grpPersonalPdf")
        pdf_layout = QVBoxLayout(self.grpPersonalPdf)
        pdf_layout.setContentsMargins(16, 18, 16, 16)
        pdf_layout.setSpacing(10)

        self.lblPdfFolder = QLabel(self.grpPersonalPdf)
        self.lblPdfFolder.setObjectName("FieldLabel")
        pdf_layout.addWidget(self.lblPdfFolder)

        pdf_folder_row = QHBoxLayout()
        pdf_folder_row.setSpacing(8)

        self.txtPdfFolderName = QLineEdit(self.grpPersonalPdf)
        self.txtPdfFolderName.setObjectName("txtPdfFolderName")
        self.txtPdfFolderName.setReadOnly(True)
        pdf_folder_row.addWidget(self.txtPdfFolderName, 1)

        self.btnBrowsePdfFolder = QPushButton(self.grpPersonalPdf)
        self.btnBrowsePdfFolder.setObjectName("btnBrowsePdfFolder")
        pdf_folder_row.addWidget(self.btnBrowsePdfFolder)
        pdf_layout.addLayout(pdf_folder_row)

        self.lblPdfPatterns = QLabel(self.grpPersonalPdf)
        self.lblPdfPatterns.setObjectName("FieldLabel")
        pdf_layout.addWidget(self.lblPdfPatterns)

        self.listPdfPatterns = QListWidget(self.grpPersonalPdf)
        self.listPdfPatterns.setObjectName("listPdfPatterns")
        self.listPdfPatterns.setMinimumHeight(72)
        pdf_layout.addWidget(self.listPdfPatterns, 1)

        pdf_buttons = QHBoxLayout()
        pdf_buttons.setSpacing(8)

        self.btnAddPdfPattern = QPushButton(self.grpPersonalPdf)
        self.btnAddPdfPattern.setObjectName("btnAddPdfPattern")
        pdf_buttons.addWidget(self.btnAddPdfPattern)

        self.btnRemovePdfPattern = QPushButton(self.grpPersonalPdf)
        self.btnRemovePdfPattern.setObjectName("btnRemovePdfPattern")
        pdf_buttons.addWidget(self.btnRemovePdfPattern)
        pdf_layout.addLayout(pdf_buttons)

        self.chkRequirePersonalPdf = QCheckBox(self.grpPersonalPdf)
        self.chkRequirePersonalPdf.setObjectName("chkRequirePersonalPdf")
        pdf_layout.addWidget(self.chkRequirePersonalPdf)
        self.grpPersonalPdf.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        right_layout.addWidget(self.grpPersonalPdf)

        self.attachmentsCard = QGroupBox(self.rightSidebar)
        self.attachmentsCard.setObjectName("attachmentsCard")
        attachments_layout = QVBoxLayout(self.attachmentsCard)
        attachments_layout.setContentsMargins(16, 18, 16, 16)
        attachments_layout.setSpacing(10)

        self.lblAttachments = QLabel(self.attachmentsCard)
        self.lblAttachments.setObjectName("FieldLabel")
        attachments_layout.addWidget(self.lblAttachments)

        attachments_buttons = QHBoxLayout()
        attachments_buttons.setSpacing(8)

        self.btnAddAttachments = QPushButton(self.attachmentsCard)
        self.btnAddAttachments.setObjectName("btnAddAttachments")
        attachments_buttons.addWidget(self.btnAddAttachments)

        self.btnClearAttachments = QPushButton(self.attachmentsCard)
        self.btnClearAttachments.setObjectName("btnClearAttachments")
        attachments_buttons.addWidget(self.btnClearAttachments)
        attachments_layout.addLayout(attachments_buttons)

        self.listAttachments = QListWidget(self.attachmentsCard)
        self.listAttachments.setObjectName("listAttachments")
        self.listAttachments.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listAttachments.setMinimumHeight(84)
        attachments_layout.addWidget(self.listAttachments, 1)
        self.attachmentsCard.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        right_layout.addWidget(self.attachmentsCard)

        self.grpRun = QGroupBox(self.rightSidebar)
        self.grpRun.setObjectName("grpRun")
        run_layout = QVBoxLayout(self.grpRun)
        run_layout.setContentsMargins(16, 18, 16, 16)
        run_layout.setSpacing(12)

        self.txtLog = QPlainTextEdit(self.grpRun)
        self.txtLog.setObjectName("txtLog")
        self.txtLog.setReadOnly(True)
        self.txtLog.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        run_layout.addWidget(self.txtLog, 1)

        self.progressBar = QProgressBar(self.grpRun)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        run_layout.addWidget(self.progressBar)
        self.grpRun.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.grpRun, 1)

    def retranslateUi(self, MainWindow: QMainWindow):
        MainWindow.setWindowTitle("AF Mailer")
        self.lblEyebrow.setText("Bulk email operations")
        self.lblHeroTitle.setText("Compose and launch personalized campaigns")
        self.lblHeroSubtitle.setText(
            "Ρύθμισε Excel δεδομένα, placeholders, προσωπικά PDFs και κάνε preview πριν στείλεις."
        )
        self.lblSummaryExcelLabel.setText("Data source")
        self.lblSummaryExcelValue.setText("No Excel loaded")
        self.lblSummaryRecipientsLabel.setText("Recipient column")
        self.lblSummaryRecipientsValue.setText("Not selected")
        self.lblSummaryAttachmentsLabel.setText("Attachments")
        self.lblSummaryAttachmentsValue.setText("0 files")
        self.lblSetupTitle.setText("Campaign setup")
        self.lblDataTitle.setText("Recipients")
        self.lblExcel.setText("Excel source")
        self.txtExcel.setPlaceholderText("Select workbook")
        self.btnBrowseExcel.setText("Browse")
        self.lblEmailCol.setText("Email column")
        self.lblMailProvider.setText("Mail account")
        self.comboMailProvider.clear()
        self.comboMailProvider.addItem("Outlook", "outlook")
        self.comboMailProvider.addItem("Gmail", "gmail")
        self.lblGmailUser.setText("Gmail address")
        self.txtGmailUser.setPlaceholderText("name@gmail.com")
        self.lblGmailPassword.setText("Gmail app password")
        self.txtGmailPassword.setPlaceholderText("16-character app password")
        self.lblGmailHint.setText("Use a Google app password, not your regular Gmail password.")
        self.grpPlaceholders.setTitle("Placeholders")
        self.lblPhHint.setText("Double click για αντιγραφή placeholder στο clipboard.")
        self.lblComposeTitle.setText("Composer")
        self.lblComposeSubtitle.setText("Στήσε το subject και το HTML body όπως σε σύγχρονο email editor.")
        self.radioDraft.setText("Save draft")
        self.radioSend.setText("Send now")
        self.txtSubject.setPlaceholderText("Email subject")
        self.btnBold.setText("B")
        self.btnItalic.setText("I")
        self.btnUnderline.setText("U")
        self.lblBody.setPlaceholderText("Write your message body here...")
        self.btnValidate.setText("Validate")
        self.btnPreview.setText("Preview")
        self.btnCheck.setText("Dry run")
        self.btnRun.setText("Start send")
        self.grpPersonalPdf.setTitle("Personal PDFs")
        self.lblPdfFolder.setText("PDF folder")
        self.txtPdfFolderName.setPlaceholderText("No folder selected")
        self.btnBrowsePdfFolder.setText("Browse")
        self.lblPdfPatterns.setText("Filename patterns")
        self.btnAddPdfPattern.setText("Add")
        self.btnRemovePdfPattern.setText("Remove")
        self.chkRequirePersonalPdf.setText("Require personal PDF for every recipient")
        self.attachmentsCard.setTitle("Shared attachments")
        self.lblAttachments.setText("Files sent to all recipients")
        self.btnAddAttachments.setText("Add files")
        self.btnClearAttachments.setText("Clear")
        self.grpRun.setTitle("Activity")
        self.txtLog.setPlaceholderText("Run logs appear here...")
