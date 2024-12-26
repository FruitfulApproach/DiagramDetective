#include "stdafx.h"
#include "DiagramChaserInteractiveScene.h"

DiagramChaserInteractiveScene::DiagramChaserInteractiveScene(QWidget *parent)
	: DiagramChaserScene(parent)
{}

DiagramChaserInteractiveScene::~DiagramChaserInteractiveScene()
{}

void DiagramChaserInteractiveScene::mouseDoubleClickEvent(QGraphicsSceneMouseEvent * event)
{
	QList<QGraphicsItem*> itemsAtMouse = items(event->scenePos());

	Node* node = nullptr;
	Semicategory* category = nullptr;

	if (itemsAtMouse.length() ==  0)
	{
		node = ambientCategory->createObject();
		node->setPos(event->scenePos());
		addItem(node);
	}
	else 
	{
		for (auto* item : itemsAtMouse)
		{
			Label* textItem = qgraphicsitem_cast<Label*>(item);
			Node* nodeParent = nullptr;

			if (textItem != nullptr)
			{
				nodeParent = qgraphicsitem_cast<Node*>(textItem->parentItem());
			}
		
			if (nodeParent == nullptr)
			{
				category = qgraphicsitem_cast<Semicategory*>(nodeParent);
			}

			if (category != nullptr)
			{
				node = category->createObject();
				node->setPos(event->scenePos());
				node->setParentItem(category);
				break;
			};
		}

		if (category == nullptr)
		{
			node = ambientCategory->createObject();
			node->setPos(event->scenePos());
			addItem(node);
		}
	}

	if (node == nullptr)
		DiagramChaserScene::mouseDoubleClickEvent(event);
}

void DiagramChaserInteractiveScene::addItem(QGraphicsItem* item)
{
	item->setFlags(item->flags() | QGraphicsItem::ItemIsMovable |
		QGraphicsItem::ItemIsSelectable | QGraphicsItem::ItemIsFocusable);

	DiagramChaserScene::addItem(item);
}