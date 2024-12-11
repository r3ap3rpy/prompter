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
            section, value = args
            print(f"Deleting {value} from the {section}!")
            if not section.lower() in self.sections:
                raise PrompterSectionDeleteException(f"The specified section {section} does not exist, these are the available sections: {','.join(self.sections)}")
            if value in self.data[section.lower()]:
                self.data[section.lower()].remove(value)
                with open(os.path.sep.join([self.module,self.folder,self.file]),'w') as jfile:
                    jfile.write(json.dumps(self.data)) 
            else:
                raise PrompterSectionDeleteException(f"The specified value {value} does not exist in section: {section}, cannot delete!")
        elif len(args) == 1:
            value = args[0]
            print(f"Deleting {value} from all the sections!")
        else:
            raise PrompterDeletionArgsError("You either have to speciy one argument to delete value from all the sections, or specify section and value to delete only from the given section.")

    def add(self, *args):
        """ You may add new entries to the data.json, the only criteria is that none of the values you specify should exist in either of the columns. """
        if len(args) != len(self.sections):
            raise PrompterAddError(f"In order to add a row you have to provide {len(self.sections)} values for the current sections: {','.join(self.sections)}")
       
        for i in range(len(args)):
            for j in self.data[list(self.sections)[i]]:
                if args[i] in self.data[list(self.sections)[i]]:
                    raise PrompterAddError(f"We already have a value {args[i]} in section {list(self.sections)[i]}")
        try:
            for i in range(len(args)):
                self.data[list(self.sections)[i]].append(args[i])
            with open(os.path.sep.join([self.module,self.folder,self.file]),'w') as jfile:
                jfile.write(json.dumps(self.data)) 
            print(f"Successfully added {','.join(args)}")
        except Exception as e:
            raise PrompterAddError(f"Failed to add new data because: {e}")

    def widest_cell(self):
        """ Returns the width of the widest cell in the table, used for formatting. """
        column_width = 0
        for key in self.data:
            if len(key) > column_width:
                column_width = len(key)
            for row in self.data[key]:
                if len(row) > column_width:
                    column_width = len(row)
        return column_width

    def longest_section(self):
        """ Returns the longest section's length. """
        return max(len(self.data[key]) for key in self.data.keys()) 

    @property
    def stats(self):
        """ Function to print short stats about sections and number of values. """
        keys = self.data.keys()
        print("#" * 47)
        for key in self.data:
            print(f"# {key:^20} # {len(self.data[key]):^20} #")
        print("#" * 47)

    @property
    def details(self, padding = 10):
        """ Detailed information about the data.json content. """
        max_length = self.longest_section()
        column_width = self.widest_cell()
        print(f"Widest cell: {column_width}")
        print("#" * (column_width * len(self.data) + padding))
        print("# " +" # ".join(f"{key:^{column_width}}" for key in self.data.keys()) + " #")
        print("#" * (column_width * len(self.data) + padding))
        for i in range(max_length):
            row = []
            for key in self.data:
                row.append(self.data[key][i] if i < len(self.data[key]) else "N.A.")
            print("# " +" # ".join(f"{key:^{column_width}}" for key in row) + " #")
        print("#" * (column_width * len(self.data) + padding))

