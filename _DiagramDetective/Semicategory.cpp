#include "stdafx.h"
#include "Semicategory.h"
#include "DiagramChaserApp.h"

Semicategory::Semicategory(const QString& name, const QString& composition, const Object* objects,
	const Arrow* arrows, QGraphicsItem *parent)
	: Object(name, parent)
{
	this->o = composition;
	this->objects = objects;
	this->arrows = arrows;
	dynamic_cast<DiagramChaserApp*>(QApplication::instance())->addCategory(this);
}

class Product:


Semicategory::~Semicategory()
{
	if (arrowSource != nullptr)
		delete arrowSource;
	if (objectSource != nullptr)
		delete objectSource;
}
