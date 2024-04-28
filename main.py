import piheaan as heaan
import os


def add_vote():
    while True:
        id = input("Pleaser enter your id: ")
        try:
            val = int(id)
            if val < 0:  # if not a positive int print message and ask for input again
                print("Sorry, input must be a positive integer, try again")
                continue
            break
        except ValueError:
            print("That's not an int!")


def compute_votes():
    pass

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

log_sots = 15
# if log_slots = 15 -> the number of slots per ciphertext is 2**15
# log_slots is used for the number of slots per ciphertext
# log_slots value depends on the parameter used. (ParameterPreset)
# 15 is the value for maximum number of slots, but you can also use a smaller number. (ex. 3, 5)
