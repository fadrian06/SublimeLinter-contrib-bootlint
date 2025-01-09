import re
from typing import Iterator

from SublimeLinter.lint import NodeLinter
from SublimeLinter.lint.linter import LintMatch


class Bootlint(NodeLinter):
    defaults = {
        "selector": "text.html.basic"
    }

    cmd = "bootlint $file_name"

    def find_errors(self, output: str) -> Iterator[LintMatch]:
        lintMatches = []
        cleanedOutput = output.replace("<", "&lt;").replace(">", "&gt;")

        for line in cleanedOutput.splitlines():
            match = re.match((
                r"(?P<filename>\w+\.\w+):"
                r"(?P<line>\d+)?:?"
                r"(?P<col>\d+)?:?"
                r" (?P<code>[A-Z\d]+)"
                r" (?P<message>.+)"
            ), line)

            if match:
                groupdict = match.groupdict()
                code = groupdict.get("code")
                errorType = "error" if not code or not code.startswith(
                    "W") else "warning"

                # print(groupdict)
                # print("\n")
                line = int(groupdict.get("line") or 1)
                col = int(groupdict.get("col") or 1)

                lintMatches.append(LintMatch({
                    "filename": groupdict.get("filename"),
                    "line": line - self.line_col_base[0],
                    "col": col - self.line_col_base[1],
                    "error_type": errorType,
                    "code": groupdict.get("code"),
                    "message": groupdict.get("message")
                }))

        # print(lintMatches)
        # print("\n")

        return iter(lintMatches)
