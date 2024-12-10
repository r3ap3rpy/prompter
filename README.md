### Welcome

This is a small module that can be used to generate prompts for text-to-image generative AI.

All you have to do is import the module and use it as follows.

``` python
from prompter import PromptGenerator
p = PromptGenerator()
'Dani Szabó volunteering at Johannesburg.'
```

You have the option to update the **data.json**.

``` python
from prompter import PromptGenerator
p = PromptGenerator()
p.update("People","Dani Ernő")
```

When updating the data the section is converted to lower-case and verified, also the value is checked whether it's in the section converted to lower-case before checking, if not it's added, otherwise an exception is thrown.

You can also delete from the **data.json** entries.

``` python
from prompter import PromptGenerator
p = PromptGenerator()
p.delete("Dani Ernő") # deletes value from every sections
p.delete("people","Pablo Picasso") # deletes value from given section
```

