import re

debug_file = open("debug.log", "w")
error_file = open("error.log", "w")
critical_file = open("critical.log", "w")


pattern = r"\b(DEBUG|ERROR|CRITICAL)\b"


with open("feature.log", "r") as log:
    for line in log:
        match = re.search(pattern, line)
        if match:
            level = match.group(1)

            if level == "DEBUG":
                debug_file.write(line)

            elif level == "ERROR":
                error_file.write(line)

            elif level == "CRITICAL":
                critical_file.write(line)


debug_file.close()
error_file.close()
critical_file.close()