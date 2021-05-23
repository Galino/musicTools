
def init():
    global AT
    global HEADER
    AT = "BQAJyqSmQvrbgo0QMMTN0nbe9JXvyyGyYSrEd3zvDSjgMDACJYj7q8Wh44XV6CvNMU873EBn0c6pKZYo0-Kx56a2NpuRMkIfejkXB3Lc5_562i97MGuBF1taY7mRVyMqjYQxYviCZptDVZSffOhmg-CNokqb4Ornob8xETuE8l3AV92oNVfPHJc2fd-xV_ay"
    HEADER = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + AT}

    print(HEADER)

init()