#include "stdafx.h"
#include "Semigroup.h"

Semigroup::Semigroup(Label* name, const QString& composition, QGraphicsItem* parent)
	: Semicategory(name, composition, parent)
{
	oneObject = nullptr;
}

Semigroup::~Semigroup()
{
	if (oneObject != nullptr)
	{
		delete oneObject;
	}
}
