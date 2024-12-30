#pragma once

#include <string>
#include <functional>
#include <map>

class Morphism;
class Variable;
class Semicategory;

class Object
{
public:
	Object(const std::string& name, const Semicategory* category=nullptr)
	{
		_name = [name]() { return name; };
		_category = category;
	}

	Object(const std::function<std::string()> name, const Semicategory* category=nullptr)
	{
		_name = name;
		_category = category;
	}

	virtual ~Object() {}

	std::string name() const { return _name(); }
	const Semicategory& category() const { return *_category; }

	virtual Object* deepcopy(std::map<const Object*, Object*> memo) const = 0;

	Morphism* operator ->() const;

protected:
	Object() {}

	friend class Variable;
	friend class Semicategory;
private:
	std::function<std::string()> _name;
	const Semicategory* _category = nullptr;			// Null pointer means the road dead ends,
	// since we don't get into universes etc.  Eventually we might assume we're in BigCat or something...
	// But then again what category is BigCat in and so on... (hence universes).
};



