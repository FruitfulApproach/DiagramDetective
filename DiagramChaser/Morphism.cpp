#include "Morphism.h"

Object* Morphism::deepcopy(std::map<const Object*, Object*> memo) const
{
	if (memo.contains(this))
		return memo[this];
	auto F = new Morphism(_domain->deepcopy(memo), _codomain->deepcopy(memo));
	memo[this] = F;
	return F;
}
