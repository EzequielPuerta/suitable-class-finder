from abc import ABC

# 	HIERARCHY				|	ATTRIBUTES			|	CONCRETE
# ==============================================================================
# Relative (Abstract)
# |
# |_ Grandfather			{name: Joe, age: 70}
# 		|
# 		|_ Aunt				{name: Jenny, age: 38}		X
# 		|
# 		|_ Uncle			{name: John, age: 45}
# 		|		|
# 		|		|_ Cousin 	{name: Jenny, age: 16}		X
# 		|
# 		|_ Father 			{name: Jack, age: 40}
# 				|
# 				|_ Me 		{name: John, age: 18}		X
# 				|
# 				|_ Brother	{name: Jeremy, age: 10}		X
# 				|
# 				|_ Sister	{name: Jenny, age: 14}		X


class Relative(ABC):  # noqa: B024
    name = ""
    age = 0

    @classmethod
    def can_handle(cls, expected_name):
        return cls.name == expected_name

    @classmethod
    def can_handle_name_and_age(cls, expected_name, expected_age):
        return (cls.name == expected_name) and (cls.age == expected_age)


class Nobody(Relative):
    name = "NN"
    age = None


class Grandfather(Relative):
    name = "Joe"
    age = 70


class Father(Grandfather):
    name = "Jack"
    age = 40


class Uncle(Grandfather):
    name = "John"
    age = 45


class Aunt(Grandfather):
    name = "Jenny"
    age = 38


class Cousin(Uncle):
    name = "Jenny"
    age = 16


class Me(Father):
    name = "John"
    age = 18


class Brother(Father):
    name = "Jeremy"
    age = 10


class Sister(Father):
    name = "Jenny"
    age = 14
