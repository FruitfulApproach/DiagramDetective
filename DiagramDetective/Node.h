#pragma once

#include <QGraphicsObject>
#include "Label.h"

class Node  : public QGraphicsObject
{
	Q_OBJECT

public:
	Node(Label* label, QGraphicsItem *parent=nullptr);

	Node(const Node& source)
		: QGraphicsObject()
	{
		if (source.label != nullptr)
		{
			this->label = new Label(*source.label);
		}

		copyStyling(source);
		setFlags(source.flags());	// BUGFIX
	}

	virtual ~Node();
	QRectF boundingRect() const override;
	void paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget = nullptr) override;
	QVariant itemChange(GraphicsItemChange change, const QVariant& value) override;
	void mouseMoveEvent(QGraphicsSceneMouseEvent* event) override;
	void mouseReleaseEvent(QGraphicsSceneMouseEvent* event) override;

	void setParentItem(QGraphicsItem* parent=nullptr)
	{
		QGraphicsObject::setParentItem(parent);
	}

	virtual QString typedName() const {
		return name() + ":" + typeName();
	}

	virtual QString typeName() const  {
		return "Node";
	}

	virtual QString longTypename() const {
		return typedName() + ":" + (
			parentItem() == nullptr ? 
			QString("") : qgraphicsitem_cast<Node*>(parentItem())->longTypename());
	}
	
	void copyStyling(const Node& source)
	{
		borderPen = source.borderPen;
		fillBrush = source.fillBrush;
		cornerRadius = source.cornerRadius;
		textFont = source.textFont;
	}

	virtual Node* copy() {
		auto node = new Node(*this);
		return node;
	}

	virtual QString name() const { return label->toPlainText(); }


public:
	// Styling
	QFont font() const { return textFont;  }
	void setFont(const QFont& font) { textFont = font;  }

private:
	void handleCollisions(const QPointF& newPos);

protected:
	// Data:
	Label* label = nullptr;

private:
	// Styling:
	QPen borderPen = QPen(QColor(51, 51, 255), 2);
	QBrush fillBrush = QBrush(QColor(255, 255, 102));
	QRectF emptyRect = QRectF(-15, -15, 30, 30);
	double cornerRadius = 15;
	QFont textFont = QFont("Serif", 17);
	
	// Collision handling:
	bool beingPushed = false;
	QSet<Node*> collisionMemo;
};
