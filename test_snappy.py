import snappy



if __name__ == '__main__':
    compressed = open('/Users/bjhl/123.snappy', 'rb').read()
    print(snappy.uncompress(compressed, 'utf-8'))