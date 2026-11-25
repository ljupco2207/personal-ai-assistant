from dataclasses import dataclass
from string import Formatter


class PromptTemplateError(ValueError):
    pass


@dataclass(frozen=True)
class PromptTemplate:
    template: str

    def render(self, **variables: str) -> str:
        required_variables = {
            field_name
            for _, field_name, _, _ in Formatter().parse(
                self.template
            )
            if field_name is not None
        }

        missing_variables = required_variables - variables.keys()

        if missing_variables:
            missing = ", ".join(sorted(missing_variables))
            raise PromptTemplateError(
                f"Missing template variables: {missing}"
            )

        return self.template.format(**variables)