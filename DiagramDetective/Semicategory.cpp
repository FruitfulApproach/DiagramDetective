#include "stdafx.h"
#include "Semicategory.h"
#include "DiagramChaserApp.h"

Semicategory::Semicategory(Label* name, const QString& compositionLaw, QGraphicsItem *parent)
	: Object(name, parent)
{
	this->o = compositionLaw;
	this->objectLabel = new Label("A");
	this->arrowLabel = new Label("a");
	this->objectSource = new Object(objectLabel);
	this->arrowSource = new Arrow(arrowLabel, nullptr, nullptr);
	dynamic_cast<DiagramChaserApp*>(QApplication::instance())->addCategory(this);
}

Semicategory::~Semicategory()
{
	if (objectLabel != nullptr)	
		delete objectLabel;
	if (arrowLabel != nullptr)
		delete arrowLabel;
	if (arrowSource != nullptr)
		delete arrowSource;
	if (objectSource != nullptr)
		delete objectSource;
}
