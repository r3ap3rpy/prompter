import json, os, random
from .customexceptions import *
dirname, filename = os.path.split(os.path.abspath(__file__))


class PromptGenerator:
    expected_sections = ['people','activity','location']
    def __init__(self, module = dirname, folder = 'data', file = 'data.json' ):
        self.module = module
        self.folder = folder
        self.file = file
        if not os.path.isfile(os.path.sep.join([module,folder,file])):
            raise PromptDataFileNotFound(f"Cannot find file {file} at location {os.path.sep.join([module,folder])}")

        try:
            with open(os.path.sep.join([module,folder,file])) as jfile:
                self.data = json.loads(jfile.read())
        except PermissionError as e:
            raise PromptDataFilePermissionError(f"Could not read the {file}, permission denied")
        except json.decoder.JSONDecodeError as e:
            raise PromptDataFileCorrupted("Invalid structure of the data, likely not json!")
        except Exception as e:
            raise Exception(f"The following error prevented initialization: {e}")

        if not self.data:
            raise PromptDataEmpty(f"The file was empty, cannot find any sections!")

        self.sections = self.data.keys()

        if self.expected_sections != list(self.sections):
            raise PromptInconsistentSectionsError(f"The source file seems to be corrupted, expected sections {','.join(self.expected_sections)} while sections in the file are {','.join(self.sections)}")
    def __call__(self):
        return f"{random.choice(self.data['people'])} {random.choice(self.data['activity']).lower()} at {random.choice(self.data['location'])}."

    def update(self, section, value):
        if not section.lower() in self.sections:
            raise PrompterSectionUpdateException(f"Either the following sections are allowed to be updated: {','.join(self.sections)}")
        if value.lower() in [ _.lower() for _ in self.data[section.lower()]]:
            raise PrompterSectionValueExists(f"The specified value: {value} is already in section: {section}, not updating")

        self.data[section.lower()].append(value)

        with open(os.path.sep.join([self.module,self.folder,self.file]),'w') as jfile:
            jfile.write(json.dumps(self.data))
    def delete(self, *args):
        if len(args) == 2:
            print(f"Deleting {args} from the given section!")
        elif len(args) == 1:
            print(f"Deleting {args} from all the sections")
        else:
            raise PrompterDeletionArgsError("You either have to speciy one argument to delete value from all the sections, or specify section and value to delete only from the given section.")


