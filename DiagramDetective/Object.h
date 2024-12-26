#pragma once

#include "Node.h"

class Object : public Node
{
	Q_OBJECT

public:
	Object(Label* label, QGraphicsItem* parent = nullptr);

	Object(const Object& source)
		: Node(source)
	{
	}

	~Object();
	QString typedName() const override { return name() + ":\\text{Object}"; }


	Node* copy() override {
		auto node = new Object(*this);
		return node;
	}
};
