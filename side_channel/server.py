from secret import PASSWORD, HASHED_PASSWORD, hash_char

guess = input("Enter {}-length password: ".format(len(PASSWORD)))

if len(guess) != len(PASSWORD):
    # handle fail

fail = False
for i, hashed_char in enumerate(HASHED_PASSWORD):
    if hashed_char != hash_char(guess[i]):
        fail = True
        break

if fail:
    # handle fail
else :
    # send flag
