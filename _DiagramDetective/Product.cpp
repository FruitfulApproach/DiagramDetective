#include "stdafx.h"
#include "ProductCategory.h"
#include <QTextDocument>
#include <format>

Product::Product(const Node* L, const Node* R, QObject *parent)
	: Semicategory("", "",parent)
{
	labelItem()->setTextFunction(() {
		return std::format("{}x{}", L->label()->text(), R->label()->text());
	});
	lhs = L;
	rhs = R;
	connect(L->label()->document(), &QTextDocument::contentsChanged, this, &ProductCategory::update);
}

ProductCategory::~ProductCategory()
{
}
