// DiagramChaser.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Semicategory.h"
#include "Variable.h"

int main()
{
    std::cout << "Hello World!\n";

    Variable A("A"), B("B");
    /*C %= new Semicategory();
    X %= Ob(C);*/

    std::cout << A.name();

    //Design: (_0->A()->B()->C()->_0) & SES;  // This adds "exact" for each internal node
    //Has same effect as (_0->A (exact)->B (exact) -> ...
}
