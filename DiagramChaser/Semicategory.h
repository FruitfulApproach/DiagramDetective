#pragma once

#include <string>
#include <functional>
#include <map>
#include "Object.h"
#include "Morphism.h"
#include "Variable.h"

class Morphism;

class Semicategory : public Object
{
public:
	Semicategory(const Object* objectType, const Morphism* arrowType, const std::string& composition = "");

	Semicategory() {
		objectType = nullptr;
		arrowType = nullptr;
		composition = "";
	}

	~Semicategory();

	Object* deepcopy(std::map<const Object*, Object*> memo) const override;

	bool is_empty() const {
		return objectType == nullptr;
	}

private:
	Object* objectType = nullptr;
	Morphism* arrowType = nullptr;
	std::string composition;
	std::function<std::string()> _name;	
	std::map<std::string, std::list<const Object*>> someObjects;
	std::map<std::string, std::list<const Morphism*>> someArrows;
};


