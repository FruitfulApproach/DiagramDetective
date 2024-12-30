#pragma once

#include "Semicategory.h"

class Semigroup  : public Semicategory
{
public:
	Semigroup(Label* name, const QString& op, QGraphicsItem *parent=nullptr);
	~Semigroup();

private:
	Object* oneObject = nullptr;
};
