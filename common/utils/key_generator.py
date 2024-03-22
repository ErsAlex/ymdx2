from passlib.pwd import genword


def codegen(lenght: int):

    code = genword(length=lenght, charset='ascii_62')
    return code
