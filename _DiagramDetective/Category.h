#pragma once

#include "Semicategory.h"
#include "Label.h"
#include "Arrow.h"

class Category  : public Semicategory
{
public:
	Category(Label* name, const QString& composition, const Object* objects,
		const Arrow* arrows, QGraphicsItem* parent = nullptr);
	~Category();
};
