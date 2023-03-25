"""Provides an environment."""

import dataclasses
import enum
import os


@enum.unique
class _Type(enum.Enum):
    CONTINUOUS_INTEGRATION = "continuous_integration"
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


@dataclasses.dataclass(frozen=True)
class _Environment:
    """Contains environment specific controls."""

    type: _Type = dataclasses.field(
        default_factory=lambda: _Type(os.getenv("ENVIRONMENT_TYPE", _Type.LOCAL.value))
    )

    @property
    def is_aws(self) -> bool:
        return self.is_development or self.is_production

    @property
    def is_production(self) -> bool:
        return self.type == _Type.PRODUCTION

    @property
    def is_development(self) -> bool:
        return self.type == _Type.DEVELOPMENT

    @property
    def is_local(self) -> bool:
        return self.type == _Type.LOCAL


environment = _Environment()
