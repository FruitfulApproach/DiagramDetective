#include "Semicategory.h"
#pragma once

Base* Semicategory::deepcopy(std::map<const Base*, Base*> memo) const
{
	if (memo.contains(this))
		return memo[this];

	auto S = new Semicategory(
		objectType->deepcopy(memo),
		dynamic_cast<Functor*>(arrowType->deepcopy(memo)), composition);

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

