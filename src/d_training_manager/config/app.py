import os
from dataclasses import dataclass
from enum import Enum


class Stage(Enum):
    Development = "dev"
    Production = "prod"
    Test = "test"


@dataclass
class AppConfig:
    @property
    def is_development(self) -> bool:
        return self.stage == Stage.Development

    @property
    def is_production(self) -> bool:
        return self.stage == Stage.Production

    @property
    def is_test(self) -> bool:
        return self.stage == Stage.Test

    @property
    def stage(self) -> Stage:
        env_stage = os.getenv("STAGE", "prod")

        for stage in Stage:
            if stage.value.lower() == env_stage.lower():
                return stage

        return Stage.Production
