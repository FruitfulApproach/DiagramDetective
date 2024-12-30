#include "stdafx.h"
#include "DiagramChaser.h"
#include "DiagramChaserApp.h"

#include "Variable.h"
#include "GlobalVars.h"


int main(int argc, char *argv[])
{
    DiagramChaserApp a(argc, argv);
    DiagramChaser w;
    w.show();

    //A %= new SemiGrp();
    //C = 

    //qDebug() << A.name() << '\n' << B.name();

    //qDebug() << (A.value())->name();

    o %= String("\circ");

    S = SemiCat(o);


    return a.exec();
}
