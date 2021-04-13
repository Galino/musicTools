
def init():
    global AT
    global HEADER
    AT = "BQDtjLxnOLhZUYt2laTsxb7R8CJnBv-cZ-UH7AXs8_Acll5AJ8Npj5s6kUM5EammdeuFAqCw_7IrYBlV1p9k73A0jHsQONlIxFm80G2Y4x-lxu39K8Iwxfeg9mvduFXAGbWyAf5IvaJsCNmIcfrUIWESvM_cG9p6UCsUFhg52wn528ZV7-3sdn9S9Rp-sWno"
    HEADER = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + AT}

    print(HEADER)

init()