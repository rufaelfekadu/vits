""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''
_pad        = '_'
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"

# phones = ["<","b","t","^","j","H","x","d","*","r","z","s","$","S","D","T","Z","E","g","f","q","k","l","m","n","h","w","y","aa","uu0","ii0","a","u0","i0","AA","A","u1","i1","<<","bb","tt","^^","jj","HH","xx","dd","**","rr","zz","ss","$$","SS","DD","TT","ZZ","EE","gg","ff","qq","kk","ll","mm","nn","hh","ww","yy",\
#     "I0","U0","UU0","II0",'U1','I1','i0i0','I0I0','u0u0','U0U0',"sil"]

ar_chars=['ى', 'ّ', 'ی', 'ت', 'ي', 'ص', 'ا', 'ش', 'ٌ', '-', 'ط', 'م', 'ق', 'ذ', 'ء', 'ٍ', 'ث', 'س', 'ج', '،', 'ْ', 'ز', 'إ', 'آ', 'ٰ', 'ض', 'ل', 'خ', 'ر', ' ', 'ظ', 'ه', 'ن', 'ئ', 'ة', 'أ', 'ِ', 'غ', 'َ', 'ب', 'ؤ', 'ً', 'و', 'ف', 'ع', 'ك', 'ُ', 'ح', 'د','\u0640']

# Export all symbols:
symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa) + ar_chars

# Special symbol ids
SPACE_ID = symbols.index(" ")
