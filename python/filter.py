def filter_words(title)
    filterwords = ["senior", "php", "ict", 'sr','electrical', 'commercial', 'commercieel','javascript', 'network', 'netwerk', 'stack']

    for word in filterwords:
        return True if word in filterwords else False