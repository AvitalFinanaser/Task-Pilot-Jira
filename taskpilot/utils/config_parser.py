from pathlib import Path

import yaml
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yml"


class AgentsConfig(BaseModel):
    model: str


class JiraConfig(BaseModel):
    url_rest_api: str
    user: str
    request_timeout: int


class ConfigModel(BaseModel):
    agents: AgentsConfig
    jira: JiraConfig


class Config:
    _instance: ConfigModel | None = None

    @classmethod
    def load(cls, path: str = "config.yml") -> None:
        if cls._instance is None:
            with open(Path(path), "r", encoding="utf-8") as config_file:
                raw_config = yaml.safe_load(config_file)
            cls._instance = ConfigModel(**raw_config)

    @classmethod
    def get(cls, path: str | Path = DEFAULT_CONFIG_PATH) -> ConfigModel:
        if cls._instance is None:
            cls.load(path)
        return cls._instance
