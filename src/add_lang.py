import os
import shutil
import pandas as pd

from translate import lang_dir_walk

REF_LANG = 'fr'

def new_lang_rst(file_path, new_lang_code):
    """
    reset the file in a starting state for a new language
    :return:
    """
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    df.rename(columns={REF_LANG: new_lang_code}, inplace=True)
    df[new_lang_code] = ''
    df['reviewed'] = False
    df.to_csv(file_path, index=False)

    new_file_name = file_path[:-len(f'{REF_LANG}.csv')] + f'{new_lang_code}.csv'
    os.rename(file_path, new_file_name)

def proc(root, target_lang):
    print(f"creating {target_lang} ", end="")
    if os.path.exists(root + target_lang):
        print(f"aborted - already exists")
        return
    shutil.copytree(root + REF_LANG, root + target_lang)
    lang_dir_walk(root + target_lang, 'new-lang', lambda x: new_lang_rst(x, target_lang))
    print(f"success")

if __name__ == "__main__":
    [proc('../', x) for x in ['ru', 'es']]
