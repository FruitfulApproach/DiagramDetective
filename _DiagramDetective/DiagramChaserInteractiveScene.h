#pragma once

#include "DiagramChaserScene.h"
#include "Node.h"
#include "DiagramChaserApp.h"

class DiagramChaserInteractiveScene  : public DiagramChaserScene
{
public:
	DiagramChaserInteractiveScene(QWidget *parent=nullptr);
	~DiagramChaserInteractiveScene();
	void addItem(QGraphicsItem* item);
	void mouseDoubleClickEvent(QGraphicsSceneMouseEvent* event) override;
};