
class Bug:
    def __init__(self, bug_id, title, description, severity, status="Open"):
        self.bug_id = bug_id
        self.title = title
        self.description = description
        self.severity = severity
        self.status = status

    def validate_report(self):
        missing_fields = []

        if self.title == "":
            missing_fields.append("title")
        if self.description == "":
            missing_fields.append("description")
        if self.severity == "":
            missing_fields.append("severity")

        if not missing_fields:
            return "VALID"
        else:
            return f"Error: The bug report is missing data in the following field(s): '{', '.join(missing_fields)}'."


def read_bug_data(file_path):
    data_list = []
    with open(file_path, "r") as f:
        for line in f:
            parts = [x.strip() for x in line.split(",")]
            # append tuple or dict, here a tuple
            data_list.append(parts)
    return data_list



def process_and_save_report(data_list, output_file):
    with open(output_file, "w") as f:
        for entry in data_list:
            bug_id, title, description, severity = entry

            bug = Bug(bug_id, title, description, severity)
            result = bug.validate_report()

            f.write(f"Bug ID {bug_id}: {result}\n")


data = read_bug_data("bugs.txt")
process_and_save_report(data, "output.txt")
