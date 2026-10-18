
import random
from collections import defaultdict

from ConfigValidator.Config.Models.RunTableModel import RunTableModel


class PairedRunTableModel(RunTableModel):
    """
    Randomize original/modified pairs while preserving stable run IDs.
    """

    def __init__(self, *args, seed=20261019, **kwargs):
        # Disable Experiment Runner's individual-row shuffle.
        kwargs["shuffle"] = False
        super().__init__(*args, **kwargs)
        self.seed = seed

    def generate_experiment_run_table(self):
        rows = super().generate_experiment_run_table()
        factors = self.get_factors()
        factor_names = [factor.factor_name for factor in factors]

        if "treatment" not in factor_names:
            raise ValueError("A treatment factor is required")

        pairs = defaultdict(list)

        for row in rows:
            run_id = row["__run_id"]

            # Standard Experiment Runner IDs:
            # run_0_repetition_0
            repetition = int(run_id.rsplit("_repetition_", 1)[1])

            key = (
                repetition,
                tuple(
                    (name, str(row[name]))
                    for name in factor_names
                    if name != "treatment"
                ),
            )

            pairs[key].append(row)

        rng = random.Random(self.seed)
        blocks = []

        for key, pair in pairs.items():
            treatments = {str(row["treatment"]) for row in pair}

            if len(pair) != 2 or treatments != {"original", "modified"}:
                raise ValueError(
                    f"Expected one original/modified pair for {key}"
                )

            blocks.append(pair)

        # Shuffle complete pairs, never individual measurements.
        rng.shuffle(blocks)

        # Guarantee exactly equal original-first and modified-first counts.
        # This is possible because the number of pairs is even.
        if len(blocks) % 2 != 0:
            raise ValueError(
                "Exactly balanced treatment ordering requires "
                "an even number of pairs"
            )

        first_treatments = (
            ["original"] * (len(blocks) // 2)
            + ["modified"] * (len(blocks) // 2)
        )
        rng.shuffle(first_treatments)

        for pair, first_treatment in zip(blocks, first_treatments):
            pair.sort(
                key=lambda row: (
                    str(row["treatment"]) != first_treatment
                )
            )

        return [row for block in blocks for row in block]
