#pragma once

#include "Object.h"
#include <map>
#include <stdexcept>
#include "Variable.h"

class Semicategory;

class Morphism : public Object
{
public:
	Morphism(const Object* domain, const Object* codomain) 
	{
		_domain = domain;
		_codomain = codomain;
	}

	Object* deepcopy(std::map<const Object*, Object*> memo) const override;

	const Object* dom() const { return _domain; }
	const Object* cod() const { return _codomain; }

	Morphism* _(Object* cod) 
	{
		if (_codomain != nullptr)
			throw std::runtime_error("Trying to set codomain of a morphism, but it's already been set.");
		
		_codomain = cod;
		return this;
	}

	Morphism* B() {
		return _(new Variable("B"));
	}

	Morphism* operator -> ()
	{
		return nullptr;
	}

	friend class Semicategory;
private:
	const Object* _domain, * _codomain;
};

