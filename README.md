# SuitableClassFinder

[![PyPI](https://img.shields.io/pypi/v/suitable-class-finder?color=blue&label=PyPI%20Version&logo=python&logoColor=white)](https://pypi.org/project/suitable-class-finder/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/EzequielPuerta/suitable-class-finder?label=Latest%20Release&display_name=tag&logo=github&logoColor=white)](https://github.com/EzequielPuerta/suitable-class-finder/releases/latest)
![GitHub License](https://img.shields.io/github/license/EzequielPuerta/suitable-class-finder?label=License&logo=github&logoColor=white)
[![Package Status](https://img.shields.io/pypi/status/suitable-class-finder.svg?label=PyPI%20Status&logo=python&logoColor=white)](https://pypi.org/project/suitable-class-finder/)
[![CircleCI](https://img.shields.io/circleci/build/gh/EzequielPuerta/suitable-class-finder/main?label=CircleCI%20Build&logo=circleci&logoColor=white)](https://circleci.com/gh/EzequielPuerta/suitable-class-finder)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/EzequielPuerta/suitable-class-finder/main?label=CodeFactor&logo=codefactor&logoColor=white)](https://www.codefactor.io/repository/github/ezequielpuerta/suitable-class-finder)
[![Codecov](https://img.shields.io/codecov/c/gh/EzequielPuerta/suitable-class-finder?label=Codecov&logo=codecov&logoColor=white)](https://codecov.io/gh/EzequielPuerta/suitable-class-finder)

Given the hierarchy of an abstract class, it detects the appropriate concrete subclass (deterministically) that satisfies certain attributes obtained as a parameter. Useful for implementing the [Strategy design pattern](https://en.wikipedia.org/wiki/Strategy_pattern).

> [!NOTE]
> This is a Python port from a useful tool which I used in my times as a Smalltalk developer and I miss a lot. It's part from a set of snippets called [Smalltools-st](https://github.com/EzequielPuerta/smalltools).

## Example

Let's imagine that we have the following hierarchy:

```python
from abc import ABC

class Vehicle(ABC):
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

class Car(Vehicle):
    def __init__(self, doors_amount, *args):
        self.doors_amount = doors_amount
        super().__init__(*args)

class Bike(Vehicle):
    pass

class Motorbike(Vehicle):
    pass
```

And we are consuming some silly API. The response could be something like:

```python
vehicles = [
    {'type':'car', 'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'type':'bike', 'doors':0, 'motor':0, 'brand':'trek', 'color':'orange'},
    {'type':'motorbike', 'doors':0, 'motor':250, 'brand':'yamaha', 'color':'black'},
    {'type':'car', 'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

Adding just this snippet to `Vehicle`:

```python
    @classmethod
    def can_handle(cls, vehicle_type):
        return cls.__name__.lower() == vehicle_type
```

...we can get the right subclass for each `json`, just passing the `type` string attribute to the `suitable_for` method:

```python
from smalltools.behavior.suitable_class_finder import SuitableClassFinder

SuitableClassFinder(Vehicle).suitable_for(vehicles[0]['type']) # Returns Car
```

> [!TIP]
> The `can_handle` method is what we called the `suitable_method` and its arguments are the `suitable_object`.

But, what if the API response is not so easy?

```python
vehicles = [
    {'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'doors':0, 'motor':0, 'brand':'trek', 'color':'orange'},
    {'doors':0, 'motor':250, 'brand':'yamaha', 'color':'black'},
    {'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

Don't worry. We can do something like this:

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    @classmethod
    @abstractmethod
    def can_handle(cls, doors, motor):
        pass

class Car(Vehicle):
    def __init__(self, doors_amount, *args):
        self.doors_amount = doors_amount
        super().__init__(*args)

    @classmethod
    def can_handle(cls, doors, motor):
        return doors > 0 and motor > 0

class Bike(Vehicle):
    @classmethod
    def can_handle(cls, doors, motor):
        return doors == 0 and motor == 0

class Motorbike(Vehicle):
    @classmethod
    def can_handle(cls, doors, motor):
        return doors == 0 and motor > 0
```

Check that you can pass multiple arguments to the `suitable_method`. So we have to do the next lines:

```python
from smalltools.behavior.suitable_class_finder import SuitableClassFinder

vehicle = vehicles[0]
SuitableClassFinder(Vehicle).suitable_for(vehicle['doors'], vehicle['motor']) # Returns Car
```

Okey, and if you have objects with different "shapes"?

```python
vehicles = [
    {'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'brand':'trek', 'color':'orange'},
    {'motor':250, 'brand':'yamaha', 'color':'black'},
    {'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

Then, you can pass the entire `json` and process it:

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    @classmethod
    @abstractmethod
    def can_handle(cls, raw_json):
        pass

class Car(Vehicle):
    def __init__(self, doors_amount, *args):
        self.doors_amount = doors_amount
        super().__init__(*args)

    @classmethod
    def can_handle(cls, raw_json):
        return 'doors' in raw_json and raw_json['doors'] > 0

class Bike(Vehicle):
    @classmethod
    def can_handle(cls, raw_json):
        return 'doors' not in raw_json and 'motor' not in raw_json

class Motorbike(Vehicle):
    @classmethod
    def can_handle(cls, raw_json):
        return 'doors' not in raw_json and 'motor' in raw_json and raw_json['motor'] > 0
```

As simple as that!

```python
from smalltools.behavior.suitable_class_finder import SuitableClassFinder

SuitableClassFinder(Vehicle).suitable_for(vehicles[0]) # Returns Car
```

The sky is the limit!

## Notes

1. The different `can_handle` cases should be disjoint. If there are many subclasses that suits to one case, it will raise an exception.
2. Subclasses should cover all possible cases. If there is a case that doesn't match with any subclass, then an exception will be thrown.
3. You can use a different method than `can_handle`. Just replace the desired method in the `suitable_method` argument of `suitable_for` function. This could be useful when you have a complex `suitable_object` and you want to be more explicit with the name of the method.
4. Sometimes, it could be good to return a default class when no result is found (instead of raising an exception). You can do this with the `default_subclass` argument of `suitable_for` method. It's disabled by default, as mentioned at the second item.
