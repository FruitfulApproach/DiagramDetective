#include "stdafx.h"
#include "DiagramChaser.h"
#include "DiagramChaserApp.h"

int main(int argc, char *argv[])
{
    DiagramChaserApp a(argc, argv);
    DiagramChaser w;
    w.show();
    return a.exec();

}
