#pragma once

#include <QGraphicsScene>
#include "Semicategory.h"

class DiagramChaserScene  : public QGraphicsScene
{
	Q_OBJECT

public:
	DiagramChaserScene(QWidget *parent=nullptr);
	~DiagramChaserScene();

	void drawBackground(QPainter* painter, const QRectF& rect) override;

protected:
	Semicategory* ambientCategory = nullptr; 
};
