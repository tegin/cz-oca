import os
import re
from typing import Any, Dict, List

from commitizen import defaults, git, config
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.cz.exceptions import CzException

__all__ = ["OCACz"]


class OCACz(BaseCommitizen):
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    commit_parser = defaults.commit_parser
    changelog_pattern = defaults.bump_pattern

    change_type_map = {
        "fix": "FIX",
        "refactor": "REF",
        "improvement": "IMP",
        "migration": "MIG",
        "openupgrade": "OU",
    }

    def questions(self) -> List[Dict[str, Any]]:
        questions: List[Dict[str, Any]] = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "FIX",
                        "name": "fix: A bug fix.",
                    },
                    {
                        "value": "IMP",
                        "name": "Improvement. A new feature.",
                    },
                    {
                        "value": "REF",
                        "name": (
                            "refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                    },
                    {
                        "value": "MIG",
                        "name": (
                            "Migration of version"
                        ),
                    },
                    {
                        "value": "OU",
                        "name": (
                            "Open Upgrade Scripts"
                        ),
                    },
                ],
            },
            {
                "type": "input",
                "name": "module",
                "message": (
                    "Module modified"
                ),
                "filter": required_validator,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": required_validator,
                "message": (
                    "Write a short and imperative summary of the code changes: (lower case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
        ]
        return questions


    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        module = answers["module"]
        subject = answers["subject"]
        body = answers["body"]
        
        if body:
            body = f"\n\n{body}"
    
        message = f"[{prefix}] {module}: {subject}{body}"

        return message

    def example(self) -> str:
        return (
            "[FIX] base: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        return (
            "[<type>] <module>: <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"[(FIX|REF|OU|MIG|IMP)]"
            r"\S+:\s.*"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:
        """add github and jira links to the readme"""
        rev = commit.rev
        m = parsed_message["message"]
        parsed_message[
            "message"
        ] = f"{m} [{rev[:5]}]"
        return parsed_message


class InvalidAnswerError(CzException):
    ...


discover_this = OCACz
