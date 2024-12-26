#pragma once

#include <QGraphicsTextItem>

class Label  : public QGraphicsTextItem
{
	Q_OBJECT

public:	
	Label(const QString& plainText, QGraphicsItem *parent=nullptr);

	Label(const Label& source)
		: QGraphicsTextItem()
	{
		this->copyFrom(source);
	}

	// void paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget);
	virtual ~Label();

	void mouseDoubleClickEvent(QGraphicsSceneMouseEvent* event)
	{
		event->ignore();
		QGraphicsTextItem::mouseDoubleClickEvent(event);
	}

	void contextMenuEvent(QGraphicsSceneContextMenuEvent* event) override;

	virtual Label* copyFrom(const Label& source)
	{
		setPlainText(source.toPlainText());
		setFont(source.font());
		return this;
	}

};
