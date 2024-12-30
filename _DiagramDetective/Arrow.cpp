#include "stdafx.h"
#include "Arrow.h"

Arrow::Arrow(Label* label, Node* domain, Node* codomain, QGraphicsItem *parent) 
	: Node(label, parent)
{
	dom = domain;
	cod = codomain;
}

Arrow::~Arrow()
{

}
