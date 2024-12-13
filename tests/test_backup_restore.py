from unittest import TestCase
from prompter.prompter import *

class BackupAndRestore(TestCase):
    def setUp(self):
        self.prompter = PromptGenerator()
        self.dirname, self.filename = os.path.split(os.path.abspath(__file__))
        self.dirname = self.dirname.replace("tests","prompter")
        self.original = os.path.sep.join([self.dirname,"data","data.json"])
    def test_backup_default(self):
        stamp = datetime.now()
        backup_file = f"{stamp.year}_{stamp.month}_{stamp.day}_{stamp.hour}_{stamp.minute}_{stamp.second}_data.json"
 
        assert self.prompter.backup_db()
        os.remove(os.path.sep.join([self.dirname,"data",backup_file]))
    def test_backup_custom_filename(self):
        temp_backup = os.path.sep.join([self.dirname,"data","temp_data.json"])
        self.prompter.backup_db(backup_file = "temp")
        assert os.path.isfile(temp_backup)
        os.remove(temp_backup)

    def test_restore_original(self):
        assert self.prompter.restore_db(original = True)

    def test_restore_custom_filename(self):
        temp_backup = os.path.sep.join([self.dirname,"data","temp_data.json"])
        self.prompter.backup_db(backup_file = "temp")
        assert self.prompter.restore_db(backup_file = "temp_data.json")
        os.remove(temp_backup)
