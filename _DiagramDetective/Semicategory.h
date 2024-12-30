#pragma once

#include "Object.h"
#include "Arrow.h"

class Semicategory  : public Object
{
	Q_OBJECT

public:
	Semicategory(const QString& name, const QString& composition, const Object* objects, 
		const Arrow* arrows, QGraphicsItem *parent=nullptr);

	Semicategory(const Semicategory& source)
		: Object(source)
	{ 
		o = source.o;
		this->objectLabel = new Label(*source.objectLabel);
		this->arrowLabel = new Label(*source.arrowLabel);
		this->objectSource = qgraphicsitem_cast<Object*>(source.objectSource->copy());
		this->arrowSource = qgraphicsitem_cast<Arrow*>(source.arrowSource->copy());
	}

	~Semicategory();

	void setArrowCopySource(Arrow* source)
	{
		arrowSource = source;
	}

	void setObjectCopySource(Object* source)
	{
		objectSource = source;
	}
	
	Object* createObject()
	{
		//objectSource = qgraphicsitem_cast<Object*>(objectSource->copy());
		//objectLabel->setParentItem(objectSource);
		return objectSource;
	}

	Arrow* createArrow()
	{
		arrowSource = qgraphicsitem_cast<Arrow*>(arrowSource->copy());
		return arrowSource;
	}

private:
	QString o;  // Guess
	Label* objectLabel = nullptr;
	Label* arrowLabel = nullptr;
	Object* objectSource = nullptr;
	Arrow* arrowSource = nullptr;
};
