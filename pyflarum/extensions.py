import typing as t

import warnings
from .error_handler import MissingExtensionError, MissingExtensionWarning



class ExtensionMixin:
    """
        A base class for mixing in custom classes (extensions) into another classes.
    """

    def __init__(self):
        self.name = "Unknown"
        self.author = "Unknown"
        self.id = "N/A"


    # TODO: Make this not require `self`, e. g. @classmethod
    def get_dependencies(self) -> t.Dict[str, t.List[object]]:
        """
            This should return the following `dict`:
            ```python
            {
                "hard": [<class>, <class>, ...],
                "soft": [<class>, <class>, ...]
            }
            ```

            A dependency is anything that you can pass into `FlarumUser(extensions=[...])` or `FlarumDatabase(extensions=[...])` (e. g. an extension class).

            #### Hard-dependencies:
            - Will raise an error when they're not found. It is impossible for the extension to function without these.

            #### Soft-dependencies:
            - Will raise just a warning. It is possible for the extension to function without these, although with limitations
            (such that some functions might be unavailable).
        """

        return {
            "hard": [],
            "soft": []
        }


    def mixin(_, class_to_patch: object, class_to_mix_in: object, skip_protected: bool=True):
        """
            A function to mix-in/merge properties, methods, functions, etc... of one class into another.

            This skips all functions and properties starting with `__` (double underscore), unless `skip_protected` is False.
            
            This sets/overwrites attributes of `class_to_patch` to attributes of
            `class_to_mix_in` (monkey-patch).

            ### Example:
            ```python
            extension.mixin(myclass, pyflarum_class)
            ```
        """

        for prop, value in vars(class_to_mix_in).items():
            if prop.startswith('__') and skip_protected:
                continue

            setattr(class_to_patch, f'{prop}', value)



def mixin_extensions(extensions: t.List[t.Type[ExtensionMixin]]) -> None:
    for extension in extensions:
        dependencies = extension.get_dependencies(extension) # type: dict

        hard = dependencies.get("hard", None)
        soft = dependencies.get("soft", None)

        if hard and len(hard) > 0:
            for hard_dependency in hard:
                if hard_dependency not in extensions:
                    raise MissingExtensionError(f'`{extension}` hardly depends on `{hard_dependency}`. Please, include that extension too in your extension list.')

        extension.mixin(extension)

        if soft and len(soft) > 0:
            for soft_dependency in soft:
                if soft_dependency not in extensions:
                    warnings.warn(f'`{extension}` softly depends on `{soft_dependency}`. Some features might be unavailable.', MissingExtensionWarning)
