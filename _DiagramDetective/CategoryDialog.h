#pragma once

#include <QDialog>
#include "ui_CategoryDialog.h"

QT_BEGIN_NAMESPACE
namespace Ui { class CategoryDialogClass; };
QT_END_NAMESPACE

class CategoryDialog : public QDialog
{
	Q_OBJECT

public:
	CategoryDialog(QWidget *parent = nullptr);
	~CategoryDialog();

public:
	Ui::CategoryDialogClass *ui;
};
