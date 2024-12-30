#include "Semicategory.h"
#include <algorithm>

Semicategory::Semicategory(const Object* objectType, const Morphism* arrowType, const std::string& composition)
{
	std::map<const Object*, Object*> memo;
	if (objectType != nullptr)
	{
		this->objectType = objectType->deepcopy(memo);
		this->objectType->_category = this;
	}
	if (arrowType != nullptr)
	{
		this->arrowType = dynamic_cast<Morphism*>(arrowType->deepcopy(memo));
		this->arrowType->_category = this;
	}
	this->composition = composition;
}

Semicategory::~Semicategory()
{
	if (objectType != nullptr)
		delete objectType;

	if (arrowType != nullptr)
		delete arrowType;

	for (auto [name, list] : someArrows)
	{
		for (const auto* f : list)
			delete f;
	}
	
	for (auto [name, list] : someObjects)
	{
		for (const auto* X : list)
			delete X;
	}
}

Object* Semicategory::deepcopy(std::map<const Object*, Object*> memo) const
{
	if (memo.contains(this))
		return memo[this];

	Object* objectType = nullptr;
	if (this->objectType != nullptr)
		objectType = this->objectType;
	
	Morphism* arrowType = nullptr;
	if (this->arrowType != nullptr)
		arrowType = this->arrowType;

	auto S = new Semicategory(objectType, arrowType, composition);

	memo[this] = S;

	for (auto [name, list] : someObjects)
	{
		for (const auto* X : list)
		{
			S->someObjects[name].push_back(X->deepcopy(memo));
		}
	}

	for (auto [name, list] : someArrows)
	{
		for (const auto* f : list)
		{
			S->someObjects[name].push_back(f->deepcopy(memo));
		}
	}

	return S;
}

