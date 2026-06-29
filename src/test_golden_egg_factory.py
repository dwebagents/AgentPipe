import pytest

from golden_egg_factory import (
    GOLDEN_EGG_UNIT_VALUE,
    GOOSE_INTRINSIC_VALUE,
    FoxAccessError,
    GoldenEggFactory,
    InvalidEggCountError,
    UnknownEggError,
)


def test_factory_starts_with_rightsized_goose_valuation():
    factory = GoldenEggFactory()

    value = factory.valuation()

    assert value.goose_value == GOOSE_INTRINSIC_VALUE == 71
    assert value.egg_value == GOLDEN_EGG_UNIT_VALUE == 3
    assert value.egg_count == 0
    assert value.total_value == 71


def test_authorized_keeper_can_lay_deterministic_golden_eggs():
    factory = GoldenEggFactory(authorized_keepers={"alice"})

    eggs = factory.lay("alice", owner="shareholders", count_value=2)

    assert [egg.egg_id for egg in eggs] == ["golden-egg-0001", "golden-egg-0002"]
    assert [egg.owner for egg in eggs] == ["shareholders", "shareholders"]
    assert [egg.value for egg in eggs] == [3, 3]
    assert factory.valuation().total_value == 77
    assert factory.audit_events() == ["laid:alice:shareholders:2"]


def test_fox_access_is_rejected_and_does_not_change_inventory():
    factory = GoldenEggFactory(authorized_keepers={"alice"})
    factory.lay("alice", owner="treasury")

    with pytest.raises(FoxAccessError):
        factory.lay("fox", owner="fox-den")

    with pytest.raises(FoxAccessError):
        factory.list_eggs("mallory")

    assert [egg.owner for egg in factory.list_eggs("alice")] == ["treasury"]
    assert factory.valuation().total_value == 74
    assert factory.audit_events()[-2:] == ["blocked:fox", "blocked:mallory"]


def test_invalid_lay_count_is_rejected_before_mutation():
    factory = GoldenEggFactory(authorized_keepers={"alice"})

    with pytest.raises(InvalidEggCountError):
        factory.lay("alice", owner="treasury", count_value=0)

    assert factory.valuation().egg_count == 0
    assert factory.audit_events() == []


def test_keeper_can_transfer_existing_egg():
    factory = GoldenEggFactory(authorized_keepers={"alice"})
    egg = factory.lay("alice", owner="treasury")[0]

    transferred = factory.transfer("alice", egg.egg_id, new_owner="ipo-vault")

    assert transferred.owner == "ipo-vault"
    assert factory.list_eggs("alice")[0].owner == "ipo-vault"
    assert factory.audit_events()[-1] == "transferred:alice:golden-egg-0001:ipo-vault"


def test_transfer_unknown_egg_does_not_create_inventory():
    factory = GoldenEggFactory(authorized_keepers={"alice"})

    with pytest.raises(UnknownEggError):
        factory.transfer("alice", "golden-egg-9999", new_owner="ipo-vault")

    assert factory.valuation().egg_count == 0
