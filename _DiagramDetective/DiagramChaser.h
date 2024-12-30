#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_DiagramChaser.h"
#include "DiagramChaserInteractiveScene.h"
#include "DiagramChaserView.h"
#include "CategoryDialog.h"


QT_BEGIN_NAMESPACE
namespace Ui { class DiagramChaserClass; };
QT_END_NAMESPACE

class DiagramChaser : public QMainWindow
{
    Q_OBJECT

public:
    DiagramChaser(QWidget *parent = nullptr);
    ~DiagramChaser();

private slots:
    void defineCategory();

private:
    Ui::DiagramChaserClass *ui;
    DiagramChaserInteractiveScene* scene = nullptr;
    DiagramChaserView* view = nullptr;
};
