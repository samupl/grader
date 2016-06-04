def parse_grader_line(line):
    """
    Parse the '# grader: ' header line for test scripts from previous grader
    version.

    :param str line: The "header" line
    :rtype: dict
    :return: A dictionary with parameters extracted from the header line
    """

    # Work our way from the end of line. First, the points parameter
    line = line.rsplit(' -- ', 1)
    points = int(line[1])

    # Remove the '# grader: ' prefix from the line
    line = line[0].replace('# grader: ', '').strip()
    line = line.split(' ', 1)

    arguments = ''
    if len(line) == 2:
        filename, arguments = line
    else:
        filename = line[0]
    return {
        'points': points,
        'filename': filename,
        'arguments': arguments
    }
