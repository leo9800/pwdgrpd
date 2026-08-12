from base import PwdgrpdTestBase
from pwdgrpd.models import GrpEntry, PwdEntry
import pytest


class TestModel(PwdgrpdTestBase):
	def test_getpwnam(self):
		u1 = self.filedb.getpwnam('eve')
		u2 = self.jsondb.getpwnam('eve')
		assert isinstance(u1, PwdEntry)
		assert isinstance(u2, PwdEntry)
		assert u1.pw_uid == 5002
		assert u2.pw_uid == 5002

	def test_getpwnam_nonexist(self):
		with pytest.raises(AssertionError, match=r'^no user named'):
			self.filedb.getpwnam('non-exist')
		with pytest.raises(AssertionError, match=r'^no user named'):
			self.jsondb.getpwnam('non-exist')

	def test_getpwuid(self):
		u1 = self.filedb.getpwuid(5000)
		u2 = self.jsondb.getpwuid(5000)
		assert isinstance(u1, PwdEntry)
		assert isinstance(u2, PwdEntry)
		assert u1.pw_name == 'alice'
		assert u2.pw_name == 'alice'

	def test_getpwuid_nonexist(self):
		with pytest.raises(AssertionError, match=r'^no user with uid'):
			self.filedb.getpwuid(2000)
		with pytest.raises(AssertionError, match=r'^no user with uid'):
			self.jsondb.getpwuid(2000)

	def test_getpwall(self):
		u1 = self.filedb.getpwall()
		u2 = self.jsondb.getpwall()
		assert set([i.pw_name for i in u1]) == set(['alice', 'bob', 'malloy', 'eve'])
		assert set([i.pw_name for i in u2]) == set(['alice', 'bob', 'malloy', 'eve'])

	def test_getgrnam(self):
		g1 = self.filedb.getgrnam('foo')
		g2 = self.jsondb.getgrnam('foo')
		assert isinstance(g1, GrpEntry)
		assert isinstance(g2, GrpEntry)
		assert set(g1.gr_mem) == set(['alice', 'bob'])
		assert set(g2.gr_mem) == set(['alice', 'bob'])

	def test_getgrnam_nonexist(self):
		with pytest.raises(AssertionError, match=r'^no group named'):
			self.filedb.getgrnam('non-exist')
		with pytest.raises(AssertionError, match=r'^no group named'):
			self.jsondb.getgrnam('non-exist')

	def test_getgrgid(self):
		g1 = self.filedb.getgrgid(7001)
		g2 = self.jsondb.getgrgid(7001)
		assert isinstance(g1, GrpEntry)
		assert isinstance(g2, GrpEntry)
		assert g1.gr_name == 'bar'
		assert g2.gr_name == 'bar'

	def test_getgrgid_nonexist(self):
		with pytest.raises(AssertionError, match=r'^no group with gid'):
			self.filedb.getgrgid(3000)
		with pytest.raises(AssertionError, match=r'^no group with gid'):
			self.jsondb.getgrgid(3000)

	def test_getgrall(self):
		g1 = self.filedb.getgrall()
		g2 = self.jsondb.getgrall()
		assert set([i.gr_name for i in g1]) == set(['alice', 'bob', 'malloy', 'eve', 'foo', 'bar', 'boo'])
		assert set([i.gr_name for i in g2]) == set(['alice', 'bob', 'malloy', 'eve', 'foo', 'bar', 'boo'])

	def test_initgroups(self):
		m1 = self.filedb.initgroups('alice')
		m2 = self.jsondb.initgroups('alice')
		assert set([i.gr_name for i in m1]) == set(['foo', 'boo'])
		assert set([i.gr_name for i in m2]) == set(['foo', 'boo'])

	def test_initgroups_nonexist(self):
		with pytest.raises(AssertionError, match=r'^no user named'):
			self.filedb.initgroups('non-exist')
		with pytest.raises(AssertionError, match=r'^no user named'):
			self.jsondb.initgroups('non-exist')

	def test_export_passwd(self):
		assert 'bob:x:5001:5001:Bob\'s Account:/home/bob:/usr/bin/bash\n' in self.filedb.to_passwd()
		assert 'bob:x:5001:5001:Bob\'s Account:/home/bob:/usr/bin/bash\n' in self.jsondb.to_passwd()

	def test_export_group(self):
		assert 'bar:x:7001:bob,eve\n' in self.filedb.to_group()
		assert 'bar:x:7001:bob,eve\n' in self.jsondb.to_group()
