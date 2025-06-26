import language_tool_python

class ContentAnalyzer:
    def __init__(self, content: str):
        self.content = content
        self.tool = language_tool_python.LanguageTool('en-US')
        self.matches = self.tool.check(content)

    def categorize_issue(self, match):
        rule_id = match.ruleId.upper()
        if "TYPOS" in rule_id or "SPELLING" in rule_id:
            return "spelling"
        elif "PUNCTUATION" in rule_id:
            return "punctuation"
        elif "STYLE" in rule_id or "REDUNDANCY" in rule_id:
            return "style"
        else:
            return "grammar"

    def analyze(self) -> dict:
        issues_by_category = {
            "spelling": [],
            "punctuation": [],
            "grammar": [],
            "style": []
        }

        counts = {
            "spelling": 0,
            "punctuation": 0,
            "grammar": 0,
            "style": 0
        }

        for match in self.matches:
            issue_type = self.categorize_issue(match)
            issues_by_category[issue_type].append({
                "message": match.message,
                "error_text": self.content[match.offset: match.offset + match.errorLength],
                "suggestions": match.replacements,
                "context": match.context
            })
            counts[issue_type] += 1

        total_issues = sum(counts.values())

        return {
            "issues": issues_by_category,
            "counts": counts,
            "total_issues": total_issues,
            "summary": f"{total_issues} language issue(s) found across grammar, spelling, punctuation, and style."
        }