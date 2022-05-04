import table as tbl

files = ("./large_texts/eng_news_100K-sentences_words.lst",
         "./large_texts/holy_grail_words.lst")

for file in files:
    root = tbl.new_empty_root()

    with open(file) as f:

        for word in f:

            tbl.add(root, word, 0)  # Value is not relevant

    print(tbl.max_depth(root))
