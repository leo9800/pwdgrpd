from typing import Literal, Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	model_config = SettingsConfigDict(
		env_prefix='PWDGRPD_',
		env_file='.env',
		env_file_encoding='utf-8',
		extra='ignore',
	)

	host: str = Field('0.0.0.0')
	port: int = Field(8000)
	source: Literal['raw', 'json'] = Field('raw')
	passwd_file: Optional[str] = Field(None)
	group_file: Optional[str] = Field(None)
	json_file: Optional[str] = Field(None)
	allow_enumeration: bool = Field(False)

	@model_validator(mode='after')
	def validate_config(self):
		if self.source == 'json':
			assert self.json_file is not None, 'json_file must be not null when use json as source'
		if self.source == 'raw':
			assert self.passwd_file is not None and self.group_file is not None, \
				'passwd_file and group_file must be both not null when use raw files as source'
		return self

config = Config() # type: ignore
