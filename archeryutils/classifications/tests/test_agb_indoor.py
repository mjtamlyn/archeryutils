"""Tests for agb indoor classification functions."""

import pytest

import archeryutils.classifications as cf
from archeryutils import load_rounds
from archeryutils.classifications.AGB_data import AGB_ages, AGB_bowstyles, AGB_genders
from archeryutils.rounds import Pass, Round

ALL_INDOOR_ROUNDS = load_rounds.read_json_to_round_dict(
    [
        "AGB_indoor.json",
        "WA_indoor.json",
    ],
)


class TestAgbIndoorClassificationScores:
    """
    Tests for the agb indoor classification scores function.

    This will implicitly check the dictionary creation.
    Provided sufficient options are covered across bowstyles, genders, and ages.
    """

    @pytest.mark.parametrize(
        "age_group,scores_expected",
        [
            (
                AGB_ages.AGE_ADULT,
                [378, 437, 483, 518, 546, 566, 582, 593],
            ),
            (
                AGB_ages.AGE_50_PLUS,
                [316, 387, 444, 488, 522, 549, 569, 583],
            ),
            (
                AGB_ages.AGE_UNDER_21,
                [316, 387, 444, 488, 522, 549, 569, 583],
            ),
            (
                AGB_ages.AGE_UNDER_18,
                [250, 326, 395, 450, 493, 526, 552, 571],
            ),
            (
                AGB_ages.AGE_UNDER_16,
                [187, 260, 336, 403, 457, 498, 530, 555],
            ),
            (
                AGB_ages.AGE_UNDER_15,
                [134, 196, 271, 346, 411, 463, 503, 534],
            ),
            (
                AGB_ages.AGE_UNDER_14,
                [92, 141, 206, 281, 355, 419, 469, 508],
            ),
            (
                AGB_ages.AGE_UNDER_12,
                [62, 98, 149, 215, 291, 364, 426, 475],
            ),
        ],
    )
    def test_agb_indoor_classification_scores_ages(
        self,
        age_group: AGB_ages,
        scores_expected: list[int],
    ) -> None:
        """Check that  classification returns expected value for a case."""
        scores = cf.agb_indoor_classification_scores(
            archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
            bowstyle=AGB_bowstyles.RECURVE,
            gender=AGB_genders.MALE,
            age_group=age_group,
        )

        assert scores == scores_expected[::-1]

    @pytest.mark.parametrize(
        "age_group,scores_expected",
        [
            (
                AGB_ages.AGE_ADULT,
                [331, 399, 454, 496, 528, 553, 572, 586],
            ),
            (
                AGB_ages.AGE_UNDER_16,
                [145, 211, 286, 360, 423, 472, 510, 539],
            ),
            (
                AGB_ages.AGE_UNDER_15,
                [134, 196, 271, 346, 411, 463, 503, 534],
            ),
            (
                AGB_ages.AGE_UNDER_12,
                [62, 98, 149, 215, 291, 364, 426, 475],
            ),
        ],
    )
    def test_agb_indoor_classification_scores_genders(
        self,
        age_group: AGB_ages,
        scores_expected: list[int],
    ) -> None:
        """
        Check that indoor classification returns expected value for a case.

        Male equivalents already checked above.
        Also checks that compound rounds are being enforced.
        """
        scores = cf.agb_indoor_classification_scores(
            archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
            bowstyle=AGB_bowstyles.RECURVE,
            gender=AGB_genders.FEMALE,
            age_group=age_group,
        )

        assert scores == scores_expected[::-1]

    @pytest.mark.parametrize(
        "bowstyle,scores_expected",
        [
            (
                AGB_bowstyles.COMPOUND,
                [472, 508, 532, 549, 560, 571, 583, 594],
            ),
            (
                AGB_bowstyles.BAREBOW,
                [331, 387, 433, 472, 503, 528, 549, 565],
            ),
            (
                AGB_bowstyles.LONGBOW,
                [127, 178, 240, 306, 369, 423, 466, 501],
            ),
            (
                # "english longbow",
                AGB_bowstyles.ENGLISHLONGBOW,
                [127, 178, 240, 306, 369, 423, 466, 501],
            ),
        ],
    )
    def test_agb_indoor_classification_scores_bowstyles(
        self,
        bowstyle: AGB_bowstyles,
        scores_expected: list[int],
    ) -> None:
        """Check that indoor classification returns expected value for a case."""
        scores = cf.agb_indoor_classification_scores(
            archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
            bowstyle=bowstyle,
            gender=AGB_genders.MALE,
            age_group=AGB_ages.AGE_ADULT,
        )

        assert scores == scores_expected[::-1]

    @pytest.mark.parametrize(
        "bowstyle,scores_expected",
        [
            (
                AGB_bowstyles.FLATBOW,
                [331, 387, 433, 472, 503, 528, 549, 565],
            ),
            (
                AGB_bowstyles.TRADITIONAL,
                [331, 387, 433, 472, 503, 528, 549, 565],
            ),
            (
                AGB_bowstyles.COMPOUNDLIMITED,
                [472, 508, 532, 549, 560, 571, 583, 594],
            ),
            (
                AGB_bowstyles.COMPOUNDBAREBOW,
                [472, 508, 532, 549, 560, 571, 583, 594],
            ),
            # Check valid bowstyle passes through coaxing unchanged.
            (
                AGB_bowstyles.RECURVE,
                [378, 437, 483, 518, 546, 566, 582, 593],
            ),
        ],
    )
    def test_agb_indoor_classification_scores_nonbowstyles(
        self,
        bowstyle: AGB_bowstyles,
        scores_expected: list[int],
    ) -> None:
        """Check that appropriate scores returned for valid but non-indoor styles."""
        coaxed_vals = cf.coax_indoor_group(
            bowstyle=bowstyle,
            gender=AGB_genders.MALE,
            age_group=AGB_ages.AGE_ADULT,
        )
        scores = cf.agb_indoor_classification_scores(
            archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
            **coaxed_vals,
        )

        assert scores == scores_expected[::-1]

    @pytest.mark.parametrize(
        "archery_round,scores_expected",
        [
            (
                ALL_INDOOR_ROUNDS["portsmouth_triple"],
                [472, 508, 532, 549, 560, 571, 583, 594],
            ),
            (
                ALL_INDOOR_ROUNDS["worcester_5_centre"],
                [217, 246, 267, 283, 294, 300, -9999, -9999],
            ),
            (
                ALL_INDOOR_ROUNDS["vegas_300_triple"],
                [201, 230, 252, 269, 281, 290, 297, 300],
            ),
        ],
    )
    def test_agb_indoor_classification_scores_triple_faces(
        self,
        archery_round: Round | str,
        scores_expected: list[int],
    ) -> None:
        """
        Check that indoor classification returns single face scores only.

        Includes check that Worcester returns null above max score.
        """
        scores = cf.agb_indoor_classification_scores(
            archery_round=archery_round,
            bowstyle=AGB_bowstyles.COMPOUND,
            gender=AGB_genders.MALE,
            age_group=AGB_ages.AGE_ADULT,
        )

        assert scores == scores_expected[::-1]

    @pytest.mark.parametrize(
        "archery_round,bowstyle,gender,age_group,msg",
        # Check all systems, different distances, negative and large handicaps.
        [
            (
                ALL_INDOOR_ROUNDS["portsmouth"],
                "invalidbowstyle",
                AGB_genders.MALE,
                AGB_ages.AGE_ADULT,
                (
                    "invalidbowstyle is not a recognised bowstyle for indoor "
                    "classifications. Please select from "
                    "`AGB_bowstyles.COMPOUND|RECURVE|BAREBOW|LONGBOW`."
                ),
            ),
            (
                ALL_INDOOR_ROUNDS["portsmouth"],
                AGB_bowstyles.RECURVE,
                "invalidgender",
                AGB_ages.AGE_ADULT,
                (
                    "invalidgender is not a recognised gender group for indoor "
                    "classifications. Please select from `archeryutils.AGB_genders`."
                ),
            ),
            (
                ALL_INDOOR_ROUNDS["portsmouth"],
                AGB_bowstyles.BAREBOW,
                AGB_genders.MALE,
                "invalidage",
                (
                    "invalidage is not a recognised age group for indoor "
                    "classifications. Please select from `archeryutils.AGB_ages`."
                ),
            ),
        ],
    )
    def test_agb_indoor_classification_scores_invalid(
        self,
        archery_round: Round | str,
        bowstyle: AGB_bowstyles,
        gender: AGB_genders,
        age_group: AGB_ages,
        msg: str,
    ) -> None:
        """Check that indoor classification returns expected value for a case."""
        with pytest.raises(
            ValueError,
            match=msg,
        ):
            _ = cf.agb_indoor_classification_scores(
                archery_round=archery_round,
                bowstyle=bowstyle,
                gender=gender,
                age_group=age_group,
            )

    def test_agb_indoor_classification_scores_invalid_round(
        self,
    ) -> None:
        """Check that indoor classification raises error for invalid round."""
        with pytest.raises(
            ValueError,
            match=(
                "This round is not recognised for the purposes of "
                "indoor classification.\n"
                "Please select an appropriate option using `archeryutils.load_rounds`."
            ),
        ):
            my_round = Round(
                "Some Roundname",
                [Pass.at_target(36, "10_zone", 122, 70.0)],
            )
            _ = cf.agb_indoor_classification_scores(
                archery_round=my_round,
                bowstyle=AGB_bowstyles.RECURVE,
                gender=AGB_genders.FEMALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    def test_agb_indoor_classification_scores_invalid_string_round(
        self,
    ) -> None:
        """Check that indoor classification raises error for invalid string round."""
        with pytest.raises(
            ValueError,
            match=(
                "This round is not recognised for the purposes of "
                "indoor classification.\n"
                "Please select an appropriate option using `archeryutils.load_rounds`."
            ),
        ):
            _ = cf.agb_indoor_classification_scores(
                archery_round="invalid_roundname",
                bowstyle=AGB_bowstyles.BAREBOW,
                gender=AGB_genders.FEMALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    def test_agb_indoor_classification_scores_string_round(
        self,
    ) -> None:
        """Check that indoor classification can process a string roundname."""
        scores = cf.agb_indoor_classification_scores(
            archery_round="portsmouth",
            bowstyle=AGB_bowstyles.COMPOUND,
            gender=AGB_genders.MALE,
            age_group=AGB_ages.AGE_ADULT,
        )

        assert scores == [472, 508, 532, 549, 560, 571, 583, 594][::-1]


class TestCalculateAgbIndoorClassification:
    """Tests for the indoor classification function."""

    @pytest.mark.parametrize(
        "score,age_group,bowstyle,class_expected",
        [
            (
                594,  # 1 above GMB
                AGB_ages.AGE_ADULT,
                AGB_bowstyles.COMPOUND,
                "I-GMB",
            ),
            (
                582,  # 1 below GMB
                AGB_ages.AGE_50_PLUS,
                AGB_bowstyles.RECURVE,
                "I-MB",
            ),
            (
                520,  # midway to MB
                AGB_ages.AGE_UNDER_21,
                AGB_bowstyles.BAREBOW,
                "I-B1",
            ),
            (
                551,  # 1 below
                AGB_ages.AGE_UNDER_18,
                AGB_bowstyles.RECURVE,
                "I-B1",
            ),
            (
                526,  # boundary value
                AGB_ages.AGE_UNDER_18,
                AGB_bowstyles.RECURVE,
                "I-B1",
            ),
            (
                449,  # Boundary
                AGB_ages.AGE_UNDER_12,
                AGB_bowstyles.COMPOUND,
                "I-B2",
            ),
            (
                40,  # Midway
                AGB_ages.AGE_UNDER_12,
                AGB_bowstyles.LONGBOW,
                "I-A1",
            ),
            (
                12,  # On boundary
                AGB_ages.AGE_UNDER_12,
                AGB_bowstyles.LONGBOW,
                "UC",
            ),
            (
                40,  # Midway
                AGB_ages.AGE_UNDER_12,
                AGB_bowstyles.ENGLISHLONGBOW,
                "I-A1",
            ),
            (
                1,
                AGB_ages.AGE_UNDER_12,
                AGB_bowstyles.ENGLISHLONGBOW,
                "UC",
            ),
        ],
    )
    def test_calculate_agb_indoor_classification(
        self,
        score: float,
        age_group: AGB_ages,
        bowstyle: AGB_bowstyles,
        class_expected: str,
    ) -> None:
        """Check that indoor classification returns expected value for a few cases."""
        class_returned = cf.calculate_agb_indoor_classification(
            score=score,
            archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
            bowstyle=bowstyle,
            gender=AGB_genders.MALE,
            age_group=age_group,
        )

        assert class_returned == class_expected

    def test_calculate_agb_indoor_classification_invalid_round(
        self,
    ) -> None:
        """Check indoor classification returns unclassified for inappropriate rounds."""
        with pytest.raises(
            ValueError,
            match=(
                "This round is not recognised for the purposes of "
                "indoor classification.\n"
                "Please select an appropriate option using `archeryutils.load_rounds`."
            ),
        ):
            _ = cf.calculate_agb_indoor_classification(
                score=400,
                archery_round="invalid_roundname",
                bowstyle=AGB_bowstyles.RECURVE,
                gender=AGB_genders.MALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    @pytest.mark.parametrize("score", [1000, 601, -1, -100])
    def test_calculate_agb_indoor_classification_invalid_scores(
        self,
        score: float,
    ) -> None:
        """Check that indoor classification fails for inappropriate scores."""
        with pytest.raises(
            ValueError,
            match=(
                f"Invalid score of {score} for a "
                f"{ALL_INDOOR_ROUNDS['portsmouth'].name}. "
                f"Should be in range 0-{ALL_INDOOR_ROUNDS['portsmouth'].max_score()}."
            ),
        ):
            _ = cf.calculate_agb_indoor_classification(
                score=score,
                archery_round=ALL_INDOOR_ROUNDS["portsmouth"],
                bowstyle=AGB_bowstyles.BAREBOW,
                gender=AGB_genders.MALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    def test_agb_indoor_classification_invalid_round(
        self,
    ) -> None:
        """Check that indoor classification raises error for invalid round."""
        with pytest.raises(
            ValueError,
            match=(
                "This round is not recognised for the purposes of "
                "indoor classification.\n"
                "Please select an appropriate option using `archeryutils.load_rounds`."
            ),
        ):
            my_round = Round(
                "Some Roundname",
                [Pass.at_target(36, "10_zone", 122, 70.0)],
            )
            _ = cf.calculate_agb_indoor_classification(
                archery_round=my_round,
                score=666,
                bowstyle=AGB_bowstyles.RECURVE,
                gender=AGB_genders.FEMALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    def test_agb_indoor_classification_scores_invalid_string_round(
        self,
    ) -> None:
        """Check that indoor classification raises error for invalid string round."""
        with pytest.raises(
            ValueError,
            match=(
                "This round is not recognised for the purposes of "
                "indoor classification.\n"
                "Please select an appropriate option using `archeryutils.load_rounds`."
            ),
        ):
            _ = cf.calculate_agb_indoor_classification(
                archery_round="invalid_roundname",
                score=666,
                bowstyle=AGB_bowstyles.BAREBOW,
                gender=AGB_genders.FEMALE,
                age_group=AGB_ages.AGE_ADULT,
            )

    def test_agb_indoor_classification_scores_string_round(
        self,
    ) -> None:
        """Check that indoor classification can process a string roundname."""
        my_class = cf.calculate_agb_indoor_classification(
            archery_round="portsmouth",
            score=578,
            bowstyle=AGB_bowstyles.COMPOUND,
            gender=AGB_genders.MALE,
            age_group=AGB_ages.AGE_ADULT,
        )

        assert my_class == "I-B1"
