#include "stdafx.h"
#include "DiagramChaserApp.h"

DiagramChaserApp::DiagramChaserApp(int& argc, char** argv)
	: QApplication(argc, argv)
{
	auto category = defaultAmbientCategoryForScenes = 
		new Category(new Label("\\textbf{BigCat}"), "\\circ ");

	semicategories[category->typedName()] = category;
}

DiagramChaserApp::~DiagramChaserApp()
{}

QStringList DiagramChaserApp::listCategoriesAlphabetically() const
{
	auto categoryList = semicategories.keys();
	std::sort(categoryList.begin(), categoryList.end());
	return categoryList;
}

