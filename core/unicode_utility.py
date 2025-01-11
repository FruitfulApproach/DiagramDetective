import string
import unicodedata


# Taken from: 
# https://stackoverflow.com/a/73427869/7076615
#
# 𝒜 (U+1D49C, MATHEMATICAL SCRIPT CAPITAL A (0xd835,0xdc9c))
# 𝓐 (U+1D4D0, MATHEMATICAL BOLD SCRIPT CAPITAL A (0xd835,0xdcd0))
# 𝒶 (U+1D4B6, MATHEMATICAL SCRIPT SMALL A (0xd835,0xdcb6))
# 𝓪 (U+1D4EA, MATHEMATICAL BOLD SCRIPT SMALL A (0xd835,0xdcea))
# 𝓏 (U+1D4CF, MATHEMATICAL SCRIPT SMALL Z (0xd835,0xdccf))
Script_A = 0x1D49C
Script_A_Bold = 0x1D4D0
Script_a = 0x1D4B6
Script_a_Bold = 0x1D4EA
Script_z = 0x1D4CF
Script_z_Bold = 0x1D503

Scripts = ''.join([chr(x) for x in range(Script_A, Script_z + 1)])
AsciiLetters = string.ascii_uppercase + string.ascii_lowercase
ScriptsTable = AsciiLetters.maketrans(AsciiLetters, Scripts)
BoldScripts = ''.join([chr(x) for x in range(Script_A_Bold, Script_z_Bold + 1)])
BoldScriptsTable = AsciiLetters.maketrans(AsciiLetters, BoldScripts)
ScriptsTable['F'] = 0x2131
print(ScriptsTable['F'])
print(ScriptsTable)

def ascii_letters_to_script(ascii_letters: str, bold: bool = False) -> str:
    if not bold:
        return ascii_letters.translate(ScriptsTable)
    else:
        return ascii_letters.translate(BoldScriptsTable)

def next_ascii_prime_variable(var: str) -> str:
    letter = var[0]        
    if 'A' <= letter < 'Z' or 'a' <= letter < 'z':
        return chr(ord(letter) + 1) + var[1:]
    elif letter == 'Z':
        return 'A' + var[1:] + "'"
    elif letter == 'z':
        return 'a' + var[1:] + "'"
    else:
        assert 0
        
        
def can_display_char(char):
    try:
        unicodedata.name(char)
        return True
    except ValueError:
        return False