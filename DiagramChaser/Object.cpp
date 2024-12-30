#include "Object.h"
#include "Morphism.h"

Morphism* Object::operator->() const
{
	return new Morphism(this, nullptr);
}