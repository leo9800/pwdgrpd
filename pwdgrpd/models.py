from functools import cached_property
from typing import Dict, List, Self
from pydantic import BaseModel, Field, computed_field


class PwdEntry(BaseModel):
	pw_name: str
	pw_passwd: str = Field(default='x')
	pw_uid: int = Field(ge=0)
	pw_gid: int = Field(ge=0)
	pw_gecos: str
	pw_dir: str
	pw_shell: str

	@classmethod
	def from_passwd(cls, i: str) -> Self:
		p = i.split(':')
		assert len(p) == 7, f'invalid passwd entry: must be 7 fields, got {len(p)}'
		return cls(
			pw_name=p[0],
			pw_passwd=p[1],
			pw_uid=int(p[2]),
			pw_gid=int(p[3]),
			pw_gecos=p[4],
			pw_dir=p[5],
			pw_shell=p[6],
		)

	def to_passwd(self) -> str:
		return f'{self.pw_name}:{self.pw_passwd}:{self.pw_uid}:{self.pw_gid}:{self.pw_gecos}:{self.pw_dir}:{self.pw_shell}'

class GrpEntry(BaseModel):
	gr_name: str
	gr_passwd: str = Field(default='x')
	gr_gid: int = Field(ge=0)
	gr_mem: List[str]

	@classmethod
	def from_group(cls, i: str) -> Self:
		p = i.split(':')
		assert len(p) == 4, f'invalid group entry: must be 7 fields, got {len(p)}'
		return cls(
			gr_name=p[0],
			gr_passwd=p[1],
			gr_gid=int(p[2]),
			gr_mem=[] if p[3] == '' else p[3].split(','),
		)

	def to_group(self) -> str:
		return f'{self.gr_name}:{self.gr_passwd}:{self.gr_gid}:{','.join(self.gr_mem)}'


class PwdGrpDatabase(BaseModel):
	pwd: List[PwdEntry]
	grp: List[GrpEntry]

	@classmethod
	def from_passwd_group(cls, p: str, g: str) -> Self:
		with open(p, 'r', encoding='utf-8') as f:
			pwd = [PwdEntry.from_passwd(i.strip()) for i in f]
		with open(g, 'r', encoding='utf-8') as f:
			grp = [GrpEntry.from_group(i.strip()) for i in f]
		return cls(pwd=pwd, grp=grp)

	def to_passwd(self) -> str:
		return '\n'.join([i.to_passwd() for i in self.pwd])

	def to_group(self) -> str:
		return '\n'.join([i.to_group() for i in self.grp])

	@computed_field
	@cached_property
	def member_of(self) -> Dict[str, List[str]]:
		d = {i.pw_name: [] for i in self.pwd}
		for i in self.grp:
			for j in i.gr_mem:
				d[j].append(i.gr_name)
		return d

	def getpwall(self) -> List[PwdEntry]:
		return self.pwd

	def getpwnam(self, name: str) -> PwdEntry:
		for i in self.pwd:
			if i.pw_name == name:
				return i
		assert False, f'no user named {name} found'

	def getpwuid(self, uid: int) -> PwdEntry:
		for i in self.pwd:
			if i.pw_uid == uid:
				return i
		assert False, f'no user with uid {uid} found'

	def getgrall(self) -> List[GrpEntry]:
		return self.grp

	def getgrnam(self, name: str) -> GrpEntry:
		for i in self.grp:
			if i.gr_name == name:
				return i
		assert False, f'no group named {name} found'

	def getgrgid(self, gid: int) -> GrpEntry:
		for i in self.grp:
			if i.gr_gid == gid:
				return i
		assert False, f'no group with gid {gid} found'

	def initgroups(self, name: str) -> List[str]:
		assert name in self.member_of, f'no user named {name} found'
		return self.member_of[name]
