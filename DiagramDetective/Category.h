#pragma once

#include "Semicategory.h"
#include "Label.h"

class Category  : public Semicategory
{
public:
	Category(Label* name, const QString& composition, QGraphicsItem* parent = nullptr);
	~Category();
};
