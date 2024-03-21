VOWELS = [
          "a", "a:", "a~", "a<", "a>", "a`", "a^", 
          "e", "e:", "e~", "e<", "e>", "e`", "e^",
          "i", "i:", "i~", "i<", "i>", "i`", "i^",
          "o", "o:", "o~", "o<", "o>", "o`", "o^",
          "u", "u:", "u~", "u<", "u>", "u`", "u^",
            ]
PROTO_UGRIC = [
    ["s<", "s"],
    ["c<"],
    ["s~"],
    ["d"],
    ["t", "tt"],
    ["d,", "t,"],
    ["mp"],
    ["p", "pp"],
    ["h>"],
    ["k", "kk"],
    ["kt", "kd"],
    ["l"],
    ["l`"],
    ["r"],
    ["m"],
    ["n"],
    ["n~"],
    ["n#"],
    ["nt"],
    ["w"],
    ["j"],
    ["jk"],
]
HUNGARIAN = [
    [["d,", "s<", "s", "z"], ["d,", "s<", "s", "z"]],
    [["c<", "d,", "s<", "s", "z<"], ["c<", "d,", "s<", "s", "z<"]], 
    [["s<", "s", "z"], ["s<", "s", "z"]],
    [["d", "l"], ["d", "l"]],
    [["d", "t"], ["z"]],
    [["d`", "j", "l,", "t,"], ["s<", "s"]],
    [["b"], ["b"]],
    [["b", "f"], ["p", "v"]],
    [["h"], ["h"]],
    [["h"], ["g", "k"]],
    [["t"], ["d"]],
    [["l"], ["l"]],
    [["l`","d,", "j"], ["l`","d,", "j"]],
    [["r"], ["r"]],
    [["m"], ["m", "v"]],
    [["n", "n~"], ["n", "n~"]],
    [["n~"], ["n~"]],
    [["g", "k", "ng", "nk", "d,", "n~", "v"], ["g", "k", "ng", "nk", "d,", "n~", "v"]],
    [["d", "t"], ["d", "t"]],
    [["v"], ["v"]],
    [["d,", "j"], ["d,", "j"]],
    [["g", "h"], ["g", "h"]],
]
KHANTY = [
    [["l", "t"],["s", "t"]],
    [["c<", "s", "t#"], ["c<", "s", "t#"]] ,
    [["s"], ["s"]],
    [["l", "t"], ["l", "t"]],
    [["t"], ["t"]],
    [["j", "t,"], ["j", "t,"]],
    [["mp"], ["mp"]],
    [["p"], ["p", "w"]],
    [["h", "k"], ["h", "k"]],
    [["h", "g", "k"], ["h", "g", "k"]],
    [["t"], ["t"]],
    [["l"], ["l"]],
    [["j", "l`", "l#"], ["j", "l`", "l#"]],
    [["r"], ["r"]],
    [["m"], ["m"]],
    [["n"], ["n"]],
    [["n~"], ["n~"]],
    [["g", "m", "n#", "n#g", "n#k", "w"], ["g", "m", "n#", "n#g", "n#k", "w"]],
    [["nt"], ["nt"]],
    [["w"], ["w"]],
    [["j"], ["j"]],
    [["g"], ["g"]],
]
MANSI = [
    [["t"], ["s", "t", "t,"]],
    [["s<", "s"], ["s<", "s"]],
    [["s"], ["s"]],
    [["l"], ["l"]],
    [["t"], ["t"]],
    [["l`", "t,"], ["l`", "t,"]],
    [["mp"], ["mp"]],
    [["p"], ["p"]],
    [["h", "k"], ["h", "k"]],
    [["h", "k"], ["h", "g", "k", "w"]],
    [["t"], ["t"]],
    [["l"], ["l"]],
    [["l`"], ["l`"]],
    [["r"], ["r"]],
    [["m"], ["m"]],
    [["n", "n~"], ["n", "n~"]],
    [["n~"], ["n~"]],
    [["g", "k", "m", "n#", "n#h", "n#k"], ["g", "k", "m", "n#", "n#h", "n#k"]],
    [["nn", "nt"], ["nn", "nt"]],
    [["w"], ["w"]],
    [["j"], ["j"]],
    [["g", "w"], ["g", "w"]]
]
SUMERIAN = [
    [["s<", "s", "z"], ["s<", "s", "z"]],
    [["s<", "s", "z"], ["s<", "s", "z"]],
    [["s<", "s", "z"], ["s<", "s", "z"]],
    [["d"], ["d"]],
    [["d", "s<", "t"], ["d", "s<", "t"]],
    [["d", "r"], ["d", "r"]],
    [["b"], ["b"]],
    [["b", "bb", "p"], ["b", "bb", "p"]],
    [["h"], ["h"]],
    [["g", "h", "k"], ["g", "h", "k"]],
    [["gg", "kk"], ["gg", "kk"]],
    [["l", "r"], ["l", "r"]],
    [["l"], ["l"]],
    [["r"], ["r"]],
    [["b", "m"], ["m"]],
    [["n"], ["n"]],
    [["n"], ["n"]],
    [["g", "j", "m", "n", "n#"], ["g", "j", "m", "n", "n#"]],
    [["d"], ["d"]],
    [["b", "m"], ["b", "m"]],
    [["j"], ["j"]],
    [["n#"], ["n#"]]
]

def check_exists(substring, lang="PU"):
    langlist = None
    if lang == "PU":
        langlist = PROTO_UGRIC
    elif lang == "H":
        langlist = HUNGARIAN
    elif lang == "H":
        langlist = HUNGARIAN
    elif lang == "VOWELS":
        langlist = VOWELS
    if langlist == None:
        return None
    
    for index, sublist in enumerate(langlist):
        if substring in sublist:
            return index
        
    return False

def generate_possibilities(counter, substring, ind, possibilities_list, char_type, rules = None, vowel_count = 0):
    if char_type == "C":
        corresponding_rule = rules[ind][0 if counter == 0 else 1]
        if counter == 0:
            temp_list = corresponding_rule
        else:
            temp_list = []
            for s in corresponding_rule:
                for c, h in enumerate(possibilities_list):
                    temp_list.append(possibilities_list[c] + s)

        return temp_list
    
    else:
        temp_list = []
        for c, h in enumerate(possibilities_list):
            if vowel_count != 1:
                temp_list.append(possibilities_list[c])
            temp_list.append(possibilities_list[c] + substring)

        return temp_list

def possibilities(PU, rules):
    possibilities_list = []
    char_type = "C"
    vowel_count = 0
    i = 0
    while i < len(PU):
        if char_type == "C":
            # check for two-part constants
            substring = PU[i:i+2]
            ind = check_exists(substring)
            if ind == None:
                break
            if ind:
                possibilities_list = generate_possibilities(i, substring, ind, possibilities_list, char_type, rules)
                i += 2
            else:
                # check for single-part constants
                substring = PU[i]
                ind = check_exists(substring)
                if ind:        
                    possibilities_list = generate_possibilities(i, substring, ind, possibilities_list, char_type, rules)
                    i+=1
            char_type = "V"

        else:
            vowel_count += 1
            substring = PU[i:i+2]
            ind = check_exists(substring, "VOWELS")
            if ind == None:
                break
            if ind:
                possibilities_list = generate_possibilities(i, substring, ind, possibilities_list, char_type, rules, vowel_count)
                i+=2
            else:
                substring = PU[i]
                possibilities_list = generate_possibilities(i, substring, ind, possibilities_list, char_type, rules, vowel_count)
                i+=1

            char_type = "C"
            
    return possibilities_list

def main():
    PU = input("Enter the Proto-Ugric word to get all possiblities of equivalents in Hungarian, Khanty, Mansi and Sumerian:\n")
    language_rules = [HUNGARIAN, KHANTY, MANSI, SUMERIAN]
    langs = ["HUNGARIAN", "KHANTY", "MANSI", "SUMERIAN"]
    for i, l in enumerate(language_rules):
        print(langs[i])
        print(possibilities(PU, l))
    

if __name__ == "__main__":
    main()