#include "Variable.h"

Variable& Variable::operator%=(Object* b)
{
	if (_assignment != nullptr)
		throw std::runtime_error(std::format("{} already assigned.", name()));
	else {
		_assignment = b;
		b->_name = [this]() { return this->name();  };
	}
	return *this;
}

Object* Variable::deepcopy(std::map<const Object*, Object*> memo) const
{
	if (memo.contains(this))
		return memo[this];
	auto v = new Variable(name());
	v->_assignment = _assignment->deepcopy(memo);
	return v;
}

