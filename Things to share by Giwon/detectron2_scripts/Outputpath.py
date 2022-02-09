import os


def outPath(inputPath):
    outpath_ph = inputPath.replace("input", "output")
    dir, file = os.path.split(outpath_ph)

    dirExist = os.path.exists(dir)
    if not dirExist:
        os.makedirs(dir)
        print("New Directory (" + dir + ") is created")

    fileExist = os.path.isfile(outpath_ph)
    if fileExist:
        outpath = generate_filename(outpath_ph, 1)
    else:
        outpath = outpath_ph

    return outpath


def generate_filename(outpath_ph, num_duplication):
    name, ext = os.path.splitext(outpath_ph)
    try_name = name + "_" + str(num_duplication) + ext

    fileExist = os.path.isfile(try_name)
    if fileExist:
        outpath = generate_filename(outpath_ph, num_duplication + 1)
    else:
        outpath = try_name

    return outpath
