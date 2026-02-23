from typing import Any, Generic, TypeVar

T = TypeVar("T")


def is_concrete(subclass: type[T]) -> bool:
    return len(subclass.__subclasses__()) == 0


def concrete_subclasses(a_class: type[T], accumulator: list[type[T]]) -> list[type[T]]:
    """For this package, concrete class is any with no subclasses.

    Parameters:
    - :a_class: : Any class object
    - :accumulator: (optional): A list with all concrete subclasses partially
    found for :a_class:

    Returns:
    - :accumulator: : List of concrete subclasses
    """
    for subclass in a_class.__subclasses__():
        if is_concrete(subclass):
            accumulator.append(subclass)
        else:
            concrete_subclasses(subclass, accumulator)
    return accumulator


class SuitableClassFinder(Generic[T]):
    """Given the hierarchy of an abstract class, it detects the appropriate
    concrete subclass (deterministically) that satisfies certain attributes
    obtained as a parameter.
    Useful for implementing the Strategy design pattern.
    """

    def __init__(self, abstract_class: type[T]) -> None:
        """Initialization of the subclass finder.

        Parameter:
        - :abstract_class: : Any class object
        """
        self.abstract_class = abstract_class
        super().__init__()

    def suitable_for(
        self,
        *suitable_object: Any,
        default_subclass: type[T] | None = None,
        suitable_method: str = "can_handle",
    ) -> type[T]:
        """Finds the concrete subclass that satisfies the conditions modeled
        with the :suitable_object: and the :suitable_method:

        Parameters:
        - :*suitable_object: : Positional arguments of any kind
        - :default_subclass: (optional): Its the object to be returned when no
        subclass is found. Keep it as :None: to ensure a match or an exception.
        - :suitable_method: (optional): Its the boolean method that tests each
        possible subclass against the :suitable_object:. It must be implemented
        in the abstract class or in its all subclasses. Keep it as :can_handle:
        for standardization.

        Returns:
        If it success, a unique subclass of the abstract class provided, which
        satisfies the :suitable_method: using the :suitable_object: as
        parameters.
        """
        all_subclasses = concrete_subclasses(self.abstract_class, [])
        filtered_subclasses = [
            subclass
            for subclass in all_subclasses
            if (getattr(subclass, suitable_method)(*suitable_object))
        ]

        subclasses_amount = len(filtered_subclasses)
        if (subclasses_amount == 0) and (default_subclass is not None):
            return default_subclass
        elif subclasses_amount == 1:
            return filtered_subclasses[0]
        elif subclasses_amount > 1:
            error = "Many subclasses can handle the suitable object '{obj}'"
            raise ValueError(error.format(obj=suitable_object))
        else:
            error = "No subclass can handle the suitable object '{obj}'"
            raise ValueError(error.format(obj=suitable_object))
