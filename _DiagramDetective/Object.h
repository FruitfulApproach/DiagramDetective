#pragma once

#include "Node.h"

class Object : public Node
{
	Q_OBJECT

public:
	Object(const QString& label, QGraphicsItem* parent = nullptr);

	Object(const Object& source)
		: Node(source)
	{
	}

	~Object() {}

	Node* copy() override {
		auto node = new Object(*this);
		return node;
	}
};
