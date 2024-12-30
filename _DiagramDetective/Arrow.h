#pragma once

#include "Node.h"
#include "Label.h"

class Arrow  : public Node
{
	Q_OBJECT

public:
	Arrow(Label* label, Node* dom, Node* cod, QGraphicsItem *parent=nullptr);
	Arrow(const Arrow& source)
		: Node(source)
	{}
	~Arrow();

	Node* copy() override 
	{
		auto node = new Arrow(*this);
		return node;
	}

private:
	Node* dom = nullptr;	Node* cod = nullptr;

};
