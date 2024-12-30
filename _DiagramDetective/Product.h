#pragma once

#include "Semicategory.h"
#include "Node.h"

class Product  : public Semicategory
{
public:
	Product(Node* L, Node* R, QGraphicsItem *parent=nullptr);
	~Product();

private:
	const Node* lhs, * rhs;
};
