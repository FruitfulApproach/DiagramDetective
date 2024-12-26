#pragma once

#include "stdafx.h"
#include <QApplication>
#include "CategoryDialog.h"
#include "Semicategory.h"

class DiagramChaserApp  : public QApplication
{
	Q_OBJECT

public:
	
	DiagramChaserApp(int& argc, char** argv);
	~DiagramChaserApp();

	Semicategory* setDefaultAmbientCategory(const QString& typedName) {
		defaultAmbientCategoryForScenes = semicategories[typedName];
	}

	Semicategory* defaultAmbientCategory() { return defaultAmbientCategoryForScenes; }

	void addCategory(Semicategory* category)
	{
		semicategories[category->name()] = category;
	}

	bool containsCategoryNamed(const QString& categoryName)
	{
		return semicategories.contains(categoryName);
	}
	
	void removeCategory(Semicategory* category)
	{
		semicategories.remove(category->name());
	}

	Semicategory* category(const QString& categoryName)
	{
		return semicategories[categoryName];
	}
	
	QStringList listCategoriesAlphabetically() const;

private:
	QMap<QString, Semicategory*> semicategories;
	Semicategory* defaultAmbientCategoryForScenes = nullptr;
};
