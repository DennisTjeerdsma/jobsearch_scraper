def filter_words(title, filterwords):
    for word in filterwords:
        if word in title.lower().split():
            return True
