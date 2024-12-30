#include "stdafx.h"
#include "Category.h"

Category::Category(Label* name, const QString& composition, const Object* objects, const Arrow* arrows, 
	QGraphicsItem *parent)
	: Semicategory(name, composition, objects, arrows, parent)	
{}

Category::~Category()
{}
