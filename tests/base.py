from pwdgrpd.models import PwdGrpDatabase


class PwdgrpdTestBase(object):
	ROOT = '/tmp/pwdgrpd-test'

	def setup_method(self, test_method):
		self.filedb = PwdGrpDatabase.from_passwd_group(
			f'{self.ROOT}/passwd',
			f'{self.ROOT}/group',
		)
		with open(f'{self.ROOT}/db.json', 'r') as f:
			self.jsondb = PwdGrpDatabase.model_validate_json(f.read())

	def teardown_method(self, test_method):
		del(self.filedb, self.jsondb)
