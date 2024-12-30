#pragma once

#include <QGraphicsObject>
#include "Label.h"
#include <functional>

class Node  : public QGraphicsObject
{
	Q_OBJECT

public:
	Node(const QString& name, QGraphicsItem* parent = nullptr);
	Node(const Node& source);
	virtual ~Node();

	QRectF boundingRect() const override;
	void paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget = nullptr) override;
	QVariant itemChange(GraphicsItemChange change, const QVariant& value) override;
	void mouseMoveEvent(QGraphicsSceneMouseEvent* event) override;
	void mouseReleaseEvent(QGraphicsSceneMouseEvent* event) override;

	virtual QString label() const {
		return _label->toPlainText();
	}

	Label* labelItem() {
		return _label;
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

public:
	// Styling
	QFont font() const { return textFont;  }
	void setFont(const QFont& font) { textFont = font;  }

private:
	void handleCollisions(const QPointF& newPos);

protected:
	// Data:
	Label* _label = nullptr;

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
