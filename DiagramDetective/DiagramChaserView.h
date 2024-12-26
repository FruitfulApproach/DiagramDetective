#pragma once

#include <QGraphicsView>

class DiagramChaserView  : public QGraphicsView
{
	Q_OBJECT

public:
	DiagramChaserView(QWidget *parent=nullptr);
	~DiagramChaserView();

	virtual bool isCurrentlyEditingScene() const {
		return false;
	}

};


class DiagramChaserInteractiveView : public DiagramChaserView
{
public:

	bool isCurrentlyEditingScene() const override {
		return true;
	}
};
