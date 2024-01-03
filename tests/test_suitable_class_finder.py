import pytest

from suitable_class_finder import (
    SuitableClassFinder,
    concrete_subclasses,
    is_concrete,
)

from .utils.suitable_class_finder import (
    Aunt,
    Brother,
    Cousin,
    Father,
    Grandfather,
    Me,
    Nobody,
    Relative,
    Sister,
    Uncle,
)


def test_is_concrete():
    assert is_concrete(Grandfather) is False
    assert is_concrete(Aunt) is True
    assert is_concrete(Uncle) is False
    assert is_concrete(Cousin) is True
    assert is_concrete(Father) is False
    assert is_concrete(Brother) is True
    assert is_concrete(Sister) is True
    assert is_concrete(Me) is True


def test_concrete_subclasses():
    assert set(concrete_subclasses(Grandfather, [])) == set(
        (
            Aunt,
            Cousin,
            Brother,
            Sister,
            Me,
        )
    )
    assert set(concrete_subclasses(Aunt, [])) == set()
    assert set(concrete_subclasses(Uncle, [])) == set((Cousin,))
    assert set(concrete_subclasses(Cousin, [])) == set()
    assert set(concrete_subclasses(Father, [])) == set((Brother, Sister, Me))
    assert set(concrete_subclasses(Brother, [])) == set()
    assert set(concrete_subclasses(Sister, [])) == set()
    assert set(concrete_subclasses(Me, [])) == set()


def test_can_handle():
    # ONLY concrete subclasses can handle the suitable object
    assert Me == SuitableClassFinder(Relative).suitable_for("John")

    # NO MORE THAN ONE concrete subclass can handle the suitable object
    with pytest.raises(ValueError):
        SuitableClassFinder(Relative).suitable_for("Jenny")

    # JUST ONE concrete subclass should handle the suitable object
    with pytest.raises(ValueError):
        SuitableClassFinder(Relative).suitable_for("Bob")


def test_default_subclass():
    # You can define a default class
    assert Nobody == SuitableClassFinder(Relative).suitable_for(
        "Bob",
        default_subclass=Nobody,
    )


def test_suitable_method():
    # You can specify an explicit canHandle method (useful for multiple
    # positional arguments)
    assert Sister == SuitableClassFinder(Relative).suitable_for(
        "Jenny",
        14,
        suitable_method="can_handle_name_and_age",
    )
