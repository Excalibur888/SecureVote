import piheaan as heaan
import os
import copy

log_sots = 2


class Voter:
    def __init__(self, id: int, ballot):
        self.id = id
        self.ballot = ballot


def print_candidates() -> int:
    count = 0
    for candidate in candidates:
        print(str(count) + ". " + candidate)
        count += 1
    return count - 1


def print_winner(result_enc):
    if result_enc == -1:
        return print("No votes to compute\n")
    result = heaan.Message(log_sots)
    dec.decrypt(result_enc, sk, result)
    max_votes = max(result, key=abs)
    max_votes_indexes = []
    for i in range(len(result)):
        if result[i] == max_votes:
            max_votes_indexes.append(int(i))
    if len(max_votes_indexes) > 1:
        print(f"Equality : ", end='')
        for i in max_votes_indexes:
            print(f"({candidates[i]})", end='')
        return print("\n")
    print(f"Winner : {candidates[max_votes_indexes[0]]}")
    return print("\n")


def add_vote():
    while True:
        _id = input("Please enter your id: ")
        try:
            id = int(_id)
            if id < 0:
                print("Sorry, your id cant be negative, try again\n")
                continue
            break
        except ValueError:
            print("That's not an id!\n")
    print("")

    for voter in votes:
        if voter.id == id:
            return -1

    while True:
        # Print candidates and get the number of candidate
        candidates_count = print_candidates()

        # Initialise ballot
        ballot = []
        for i in range(candidates_count + 1):
            ballot.append(int(0))

        # User input for candidate
        _vote = input("Please choose your candidate: ")
        try:
            vote = int(_vote)
            if vote < 0 or vote > candidates_count:
                print("Sorry, your number is not valid, try again\n")
                continue
            break
        except ValueError:
            print("That's not an number!\n")

    # Flag the candidate in the ballot
    ballot[vote] = 1

    ballot_enc = heaan.Message(log_sots)
    for i in range(len(ballot)):
        ballot_enc[i] = int(ballot[i])

    # encrypt m1 to ctxt1 using public_key
    ctxt = heaan.Ciphertext(context)
    enc.encrypt(ballot_enc, pk, ctxt)

    return Voter(id, ctxt)


def compute_votes():
    if len(votes) == 0:
        return -1
    result = heaan.Ciphertext(context)
    result.log_slots = log_sots
    for v in range(len(votes)):
        eval.add(result, votes[v].ballot, result)
    return result


# set parameter
params = heaan.ParameterPreset.FGb
context = heaan.make_context(params)  # context has parameter information
heaan.make_bootstrappable(context)  # Make parameter bootstrapable

key_file_path = "./keys"
# create secret_keys
sk = heaan.SecretKey(context)  # create secret key
os.makedirs(key_file_path, mode=0o775, exist_ok=True)

# create public_key
key_generator = heaan.KeyGenerator(context, sk)
key_generator.gen_common_keys()

pk = key_generator.keypack

eval = heaan.HomEvaluator(context, pk)  # to load pi-heaan math
dec = heaan.Decryptor(context)  # for decrypt
enc = heaan.Encryptor(context)  # for encrypt

votes = []
candidates = ["Lee Jae-myung", "Lee Nak-yeon", "Park Yong-jin", "Choo Mi-ae"]

while True:
    menu = input("1. Vote\n2. Results\n3. Exit\nPlease select one action: ")
    menu = int(menu)
    if menu == 1:
        vote = add_vote()
        if vote == -1:
            print("You have already voted.\n")
        else:
            votes.append(vote)
            print("Vote added !\n")
        continue
    if menu == 2:
        print_winner(compute_votes())
        continue
    if menu == 3:
        exit()
    if menu != 1 and menu != 2 and menu != 3:
        print("Invalid option\n")
        continue
