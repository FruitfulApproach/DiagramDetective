#include "stdafx.h"
#include "CategoryDialog.h"

CategoryDialog::CategoryDialog(QWidget* parent)
	: QDialog(parent)
	, ui(new Ui::CategoryDialogClass())
{
	ui->setupUi(this);
	connect(ui->buttonBox, &QDialogButtonBox::accepted, this, &CategoryDialog::accept);
	connect(ui->buttonBox, &QDialogButtonBox::rejected, this, &CategoryDialog::reject);
}

CategoryDialog::~CategoryDialog()
{
	delete ui;
}
