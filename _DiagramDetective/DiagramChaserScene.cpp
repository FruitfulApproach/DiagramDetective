#include "stdafx.h"
#include "DiagramChaserScene.h"
#include "DiagramChaserApp.h"

DiagramChaserScene::DiagramChaserScene(QWidget *parent)
	: QGraphicsScene(parent)
{

	ambientCategory = qobject_cast<DiagramChaserApp*>(QApplication::instance())->defaultAmbientCategory();
}

DiagramChaserScene::~DiagramChaserScene()
{}

void DiagramChaserScene::drawBackground(QPainter * painter, const QRectF & rect)
{
	painter->setRenderHint(QPainter::TextAntialiasing);
	QFont f = font();
	f.setBold(true);
	painter->setFont(f);
	painter->drawText(QPoint(), ambientCategory->typedName());
}
