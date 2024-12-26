#include "stdafx.h"
#include "Category.h"

Category::Category(Label* name, const QString& composition, QGraphicsItem *parent)
	: Semicategory(name, composition, parent)	
{}

Category::~Category()
{}
