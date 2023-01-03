import os
from cleantext import clean

junks = ("Message-ID", "Date", "From", "To", "Cc", "Mime-Version", "Content-Type", "Bcc", "X-From", "X-To", "X-bcc", "X-Folder", "X-Origin", "X-FileName", "X-cc", "Content-Transfer-Encoding", "Email")
folders= os.listdir("./data")

# def remove_special(data):
    # normal_string="".join(ch for ch in data if ch.isalnum() or ch == " ")
    # return normal_string
    
def clean_text(data):
    cleaned = clean(data,
                fix_unicode=True,               # fix various unicode errors
                to_ascii=True,                  # transliterate to closest ASCII representation
                lower=True,                     # lowercase text
                no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
                no_urls=True,                  # replace all URLs with a special token
                no_emails=True,                # replace all email addresses with a special token
                no_phone_numbers=False,         # replace all phone numbers with a special token
                no_numbers=False,               # replace all numbers with a special token
                no_digits=False,                # replace all digits with a special token
                no_currency_symbols=False,      # replace all currency symbols with a special token
                replace_with_url=" ",
                replace_with_email=" ",
                replace_with_phone_number=" ",
                replace_with_number=" ",
                replace_with_digit=" ",
                replace_with_currency_symbol=" ",
                #no_punct=True,                 # remove punctuations
                #replace_with_punct="",          # instead of removing punctuations you may replace them
                lang="en"                       # set to 'de' for German special handling
            )
    
    return cleaned+" "

for folder in folders:
    files = os.listdir("./data/"+folder)
    #print(files)
    for file in files:
        if ".txt" in file:
            print(file)
            with open("./data/"+folder+"/"+file, "r") as f:
                lines = f.readlines()
                lines = [clean_text(line) for line in lines if not any(junk in line for junk in junks) ]
                #print(lines)
                
                
                with open("./data/cleaned/"+folder+"/cleaned_"+file, "w+") as g:
                    g.writelines(lines)

#balancing data and compiling in single csv
folders = os.listdir("./data/cleaned/")
print(folders)

df = pd.DataFrame(columns = ['label','text'])

for folder in folders:
    #print("\n\n\nSampled")
    sampled_files = os.listdir("./data/cleaned/"+folder+"/")
    #print(sampled_files, len(sampled_files))
    if len(sampled_files)<834:
        t = math.ceil(834/len(sampled_files))
    else:
        t=1
    for file in sampled_files:
        with open("./data/cleaned/"+folder+"/"+file, "r") as f:
            data = f.read()
            for _ in range(t):
                df = df.append({'label': str(int(folder)-1), 'text' : data}, ignore_index = True)
print(df)
df = df.sample(frac = 1)
df.to_csv("data_balanced.csv", index=0)
