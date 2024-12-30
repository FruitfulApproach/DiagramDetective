#pragma once

#include <QGraphicsTextItem>

class Label  : public QGraphicsTextItem
{
	Q_OBJECT

public:	
	Label(const QString& text, QGraphicsItem *parent=nullptr);

	Label(const Label& source)
		: QGraphicsTextItem(source.toPlainText(), source.parentItem())
	{
		this->copyFrom(source);
	}

	QString text() const { return toPlainText();  }

	void setTextFunction(std::function<QString()> textFunc)
	{
		this->textFunc = textFunc;
		isDynamic = true;
		update();
	}

	void setPlainText(const QString& text);

	void update() {
		if (isDynamic)
			setPlainText(textFunc());
		QGraphicsTextItem::update();
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
		setFont(source.font());
		return this;
	}

private:
	std::function<QString()> textFunc;
	bool isDynamic = false;
	bool editLocked = false;
};
