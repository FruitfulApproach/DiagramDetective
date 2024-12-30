#pragma once

#include <string>
#include "Object.h"
#include <stdexcept>
#include <format>

class Object;

class Variable : public Object
{
public:
	Variable(const std::string& name) : Object(name) {}
	virtual ~Variable() {}
	Variable& operator %= (Object* b);
	Object* deepcopy(std::map<const Object*, Object*> memo) const override;

private:
	Object* _assignment = nullptr;
};

