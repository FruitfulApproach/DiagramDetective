#include "stdafx.h"
#include "DiagramChaserInteractiveScene.h"
#include "DiagramChaserView.h"


Label::Label(const QString& text, QGraphicsItem *parent)
	: QGraphicsTextItem(text, parent)
{
	setFont(QFont("Serif", 17));
}

//void Label::paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget)
//{
//
//	//{
//	//	painter->setRenderHint(QPainter::TextAntialiasing);
//	//	painter->setPen(borderPen);
//	//	painter->setBrush(fillBrush);
//	//	painter->drawRoundedRect(boundingRect(), cornerRadius, cornerRadius);
//	//}
//}

void Label::setPlainText(const QString& text)
{
	if (!editLocked)
		QGraphicsTextItem::setPlainText(text);
	else
		throw std::runtime_error("Programmer Error: trying to setPlainText() on an editLocked Label instance.");
}

Label::~Label()
{}


void Label::contextMenuEvent(QGraphicsSceneContextMenuEvent* event)
{
	if (scene())
	{
		if (dynamic_cast<DiagramChaserInteractiveScene*>(scene()))
		{
			foreach (QGraphicsView* view, scene()->views())
			{
				auto chaserView = dynamic_cast<DiagramChaserView*>(view);

				if (chaserView != nullptr)
				{
					if (chaserView->isCurrentlyEditingScene())
					{
						QMenu menu(chaserView);
						menu.addAction("Test");

						menu.exec(chaserView->mapToGlobal(chaserView->mapFromScene(event->scenePos())));
						break;
					}
				}
			}
		}
	}
}
