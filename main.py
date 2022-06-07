from genericpath import exists
import re
import zipfile
import tempfile
import os

REGEX = r"^.*?\["\
    r"((23/Mar/2009:("\
    r"(03:[4-5][0-9]:\d{2})"\
    r"|(03:3[8-9]:\d{2})"\
    r"|(03:38:[1-9][0-9])"\
    r"|((0[3-9])|[12][0-9]:\d{2}:\d{2})"\
    r"))|((2[4-9])/Mar/2009:\d{2}:\d{2}:\d{2})"\
    r"|(30/Mar/2009:("\
    r"(12:0[0-9]:\d{2})"\
    r"|(12:1[0-2]:\d{2})"\
    r"|(12:13:[1-4][0-9])"\
    r"|((0[0-9])|(10)|(11):\d{2}:\d{2})"\
    r")))"\
        r".*\"GET .*\" 200 .*?photo.*?$"

# REGEX = r"^.*?\["\
#     r"((02/Mar/2004:("\
#     r"(09:14:5[6-9])"\
#     r"|(09:1[5-9]:\d{2})"\
#     r"|(09:[2-9][0-9]:\d{2})"\
#     r"|([12][0-9]:\d{2}:\d{2})"\
#     r"))|((0[3-9])|(1[0-4])/Mar/2004:\d{2}:\d{2}:\d{2})"\
#     r"|(15/Mar/2004:("\
#     r"((0[0-9])|(10)|(11):\d{2}:\d{2})"\
#     r"|(12:0[0-9]:\d{2})"\
#     r"|(12:10:\d{2})"\
#     r"|(12:12:[0-4][0-9])"\
#     r"|(12:12:5[0-5])"\
#     r")))"\
#         r".*\"GET .*\" 200 .*?TWiki.*?$"

def print_out_from_text_with_regex(string: str, regex: str) -> None:
    """Print out all regex matches in standard output

    Args:
        string (str): Text to search regex
        regex (str): Regex string using for search
    """
    matches = re.finditer(regex, string, re.MULTILINE)

    matches = list(matches)
    if len(matches) == 0:
        print("There are not any occurence of the regex in the file")
    else:
        for index, match in enumerate(matches, start=1):
            print(f"{index}. {match.group()}")


def main():
    filename = input('Enter path to the file: ')

    filename = filename.strip()
    if not exists(filename):
        raise FileExistsError("File don't exist or unreacheable")

    if re.match(r".*\.zip$", filename) is not None:
        with zipfile.ZipFile(filename, mode='r') as archive:
            tmp_dir = tempfile.mkdtemp()
            archive.extractall(tmp_dir)
            logs_from_archive = [os.path.join(tmp_dir, logfile) for logfile in os.listdir(
                tmp_dir) if os.path.isfile(os.path.join(tmp_dir, logfile))]

            for filename in logs_from_archive:
                print(f"From file: {filename}")
                with open(filename, encoding='UTF-8') as file:
                    text = file.read()
                    print_out_from_text_with_regex(text, REGEX)
                print()
    else:
        with(open(filename, mode='r', encoding='UTF-8')) as file:
            text = file.read()
            print_out_from_text_with_regex(text, REGEX)


if __name__ == '__main__':
    main()
